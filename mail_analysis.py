import imaplib
import email
from email.header import decode_header
import json
from email.utils import parsedate_to_datetime
import os
from dotenv import load_dotenv
from summarization import TEXT

load_dotenv(".env")

# Email credentials and server details
email_address = os.getenv('MAIL')
email_password = os.getenv('PASSWORD')
imap_server = os.getenv('SERVER')
imap_port = int(os.getenv('PORT'))

# List of keywords to filter emails
keyword_list = ["GTU"]

# Connect to the IMAP server
mail = imaplib.IMAP4_SSL(imap_server, imap_port)
mail.login(email_address, email_password)

# Select the mailbox you want to access (e.g., 'inbox')
mail.select("inbox")

# Search for the latest 10 emails in the mailbox
status, messages = mail.search(None, "ALL")
messages = messages[0].split()
messages.reverse()

# Initialize a list to store filtered email information
filtered_email_list = []

# Fetch and process each email
for email_id in messages:
    status, msg_data = mail.fetch(email_id, "(RFC822)")

    # Parse the email content
    raw_email = msg_data[0][1]
    email_message = email.message_from_bytes(raw_email)

    # Get sender's name, email address, subject, date, and time
    sender_name, sender_email = email.utils.parseaddr(email_message["From"])

    # Decode subject with a default encoding if it's None
    subject, encoding = decode_header(email_message["Subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding or "utf-8")

    # Get date and time of receiving email
    date_time_received = parsedate_to_datetime(email_message["Date"])
    date_received = date_time_received.strftime("%d-%m-%Y")
    time_received = date_time_received.strftime("%H:%M")

    # Get the body of the email
    if email_message.is_multipart():
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode("utf-8")
                break
    else:
        body = email_message.get_payload(decode=True).decode("utf-8")

    # Check if any keyword is present in the body
    if any(keyword.lower() in body.lower() for keyword in keyword_list):
        # Store email information in a dictionary
        email_info = {
            "SenderName": sender_name,
            "SenderEmail": sender_email,
            "Subject": subject,
            "Date": date_received,
            "Time": time_received
        }

        print(email_info)
        print('-'*200)

        # Add the dictionary to the list
        filtered_email_list.append(email_info)

# Output the filtered information in JSON format
output_json = json.dumps(filtered_email_list, indent=2)
print(output_json)

# Logout from the server
mail.logout()
