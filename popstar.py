import imaplib
import email
import os
from dotenv import load_dotenv
import re

load_dotenv('.env')

# IMAP server settings
IMAP_SERVER = os.getenv('IMAP_SERVER')
EMAIL = os.getenv('MAIL')
PASSWORD = os.getenv('PASSKEY')

# Connect to the IMAP server
mail = imaplib.IMAP4_SSL(IMAP_SERVER)

# Login to your account
mail.login(EMAIL, PASSWORD)

# Select the mailbox (in this case, the "INBOX")
mail.select('inbox')

# Search for all emails in the "Primary" folder
result, data = mail.search(None, 'ALL')

phone_number_pattern = re.compile(r'\b(?:\+?91|0)?\d{10}\b')

if result == 'OK':
    for num in data[0].split():
        result, data = mail.fetch(num, '(RFC822)')
        if result == 'OK':
            email_message = email.message_from_bytes(data[0][1])
            print('From:', email_message['From'])
            print('Subject:', email_message['Subject'])
            # Iterate over each part of the email (plaintext or multipart)
            for part in email_message.walk():
                content_type = part.get_content_type()
                if content_type == 'text/plain':
                    email_body = part.get_payload(decode=True).decode(part.get_content_charset())
                    print('Body:', email_body)
                    # Extract phone numbers from the email body
                    phone_numbers = phone_number_pattern.findall(email_body)
                    if phone_numbers:
                        print('Phone Numbers:', phone_numbers)
                else:
                    filename = part.get_filename()
                    if filename:
                        print('Attachment:', filename, 'Type:', content_type)
            print('------------------------------------------')

# Logout from the server
mail.logout()
