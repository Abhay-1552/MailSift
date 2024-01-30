import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv
from email import policy
from email.parser import BytesParser

load_dotenv(".env")


def get_text_body(payload):
    if payload.is_multipart():
        # Iterate over parts and get the first "text/plain" or "text/html" part
        for part in payload.iter_parts():
            if part.get_content_type() in ["text/plain", "text/html"]:
                return part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8')
    else:
        # If the message is not multipart, return the plain text payload
        return payload.get_payload(decode=True).decode(payload.get_content_charset() or 'utf-8')


def get_email_body(username, password, server, port, mailbox="INBOX", search_criteria="(UNSEEN)"):
    # Connect to the IMAP server
    mail = imaplib.IMAP4_SSL(server, port)

    # Login to the email account
    mail.login(username, password)

    # Select the mailbox (default is INBOX)
    mail.select(mailbox)

    # Search for unread emails based on the search criteria
    status, messages = mail.search(None, search_criteria)

    # Get the list of email IDs
    email_ids = messages[0].split()

    for email_id in email_ids:
        # Fetch the email by ID
        status, msg_data = mail.fetch(email_id, "(RFC822)")

        # Get the email content
        raw_email = msg_data[0][1]
        email_message = BytesParser(policy=policy.default).parsebytes(raw_email)

        # Get the subject
        subject, encoding = decode_header(email_message["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8")

        print(f"Subject: {subject}, Message: {email_message}")

        # Get the body payload text
        # body_text = get_text_body(email_message)
        # print("Body Payload Text:")
        # print(body_text)

    # Logout from the email server
    mail.logout()


# Example usage
username = os.getenv('MAIL')
password = os.getenv('PASSWORD')
server = os.getenv('SERVER')
port = int(os.getenv('PORT'))

get_email_body(username, password, server, port)
