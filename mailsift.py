import imaplib
import email
from email.header import decode_header
from email.utils import parsedate_to_datetime
import os
from dotenv import load_dotenv
import pandas as pd
import json
import re
from bs4 import BeautifulSoup
from tqdm import tqdm
import sys
from datetime import datetime


class Mail:
    def __init__(self):
        load_dotenv(".env")

        self.email_address = os.getenv('MAIL')
        self.email_password = os.getenv('PASSKEY')
        self.imap_server = os.getenv('IMAP_SERVER')
        self.imap_port = int(os.getenv('IMAP_PORT'))

        self.mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
        self.mail.login(self.email_address, self.email_password)

    def mail_data(self):
        try:
            self.mail.select("inbox")

            start_date = datetime(2024, 3, 1)  # Start date (YYYY, MM, DD)
            end_date = datetime(2024, 3, 25)  # End date (YYYY, MM, DD)

            search_query = f'(SINCE {start_date.strftime("%d-%b-%Y")}) (BEFORE {end_date.strftime("%d-%b-%Y")})'

            # Search for the latest 10 emails in the mailbox
            status, messages = self.mail.search(None, search_query)
            messages = messages[0].split()
            messages.reverse()
            top_messages = messages[:]

            filtered_email_list = []
            # Fetch and process each email
            for email_id in tqdm(top_messages):
                status, msg_data = self.mail.fetch(email_id, "(RFC822)")

                # Parse the email content
                raw_email = msg_data[0][1]
                email_message = email.message_from_bytes(raw_email)

                # Get sender's name, email address, subject, date, and time
                sender_name, sender_email = email.utils.parseaddr(email_message["From"])
                sender_name = sender_name or "Unknown Sender"
                sender_email = sender_email or "unknown@example.com"

                # Decode subject with a default encoding if it's None
                subject, encoding = decode_header(email_message["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or "utf-8")

                    # Changing specials characters in heading
                    # subject = re.sub(r'[^\x00-\x7F]+', '<Special Characters>', subject)

                # Get date and time of receiving email
                date_time_received = parsedate_to_datetime(email_message["Date"])
                date_received = date_time_received.strftime("%d-%b-%Y")
                time_received = date_time_received.strftime("%H:%M")

                decoded_payload = " "

                # Get the body of the email, prioritizing text/plain parts
                if email_message.is_multipart():
                    for part in email_message.get_payload():
                        content_type = part.get_content_type()
                        if content_type == "text/plain":
                            decoded_payload += part.get_payload(decode=True).decode(
                                part.get_content_charset() or "utf-8", errors="ignore")

                        elif content_type == "text/html":
                            html_payload = part.get_payload(decode=True)
                            soup = BeautifulSoup(html_payload, 'html.parser')
                            if soup.body:
                                main_content = soup.body.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span'])
                                data = ''
                                for content in main_content:
                                    data += content.get_text(strip=True) + ' '
                                decoded_payload += data

                        elif content_type.startswith('image/'):
                            filename = part.get_filename()
                            decoded_payload += f"Image Attachment: {filename}, Content Type: {content_type}\t"

                        elif content_type.startswith('application/'):
                            filename = part.get_filename()
                            decoded_payload += f"Document Attachment: {filename}, Content Type: {content_type}\t"
                else:
                    if email_message.get_content_type() == "text/plain":
                        decoded_payload += email_message.get_payload(decode=True).decode(
                            email_message.get_content_charset() or "utf-8", errors="ignore")

                    elif email_message.get_content_type() == "text/html":
                        html_payload = email_message.get_payload(decode=True)
                        soup = BeautifulSoup(html_payload, 'html.parser')
                        if soup.body:
                            main_content = soup.body.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span'])
                            data = ''
                            for content in main_content:
                                data += content.get_text(strip=True) + ' '
                            decoded_payload += data

                    elif email_message.get_content_type().startswith('image/'):
                        attachment_filename = email_message.get_filename()
                        decoded_payload += f"Image Attachment: {attachment_filename}, Content Type: {email_message.get_content_type()}\t"

                    elif email_message.get_content_type().startswith('application/'):
                        attachment_filename = email_message.get_filename()
                        decoded_payload += f"Document Attachment: {attachment_filename}, Content Type: {email_message.get_content_type()}\t"

                    else:
                        decoded_payload += "<Unsupported Content or Blank Mail>"

                pattern = r'\b(?:\+91|0)?[789]\d{9}\b'
                phone_numbers = re.findall(pattern, decoded_payload)

                cleaned_payload = Mail.cleaning_mail(decoded_payload)

                email_info = {
                    "SenderName": sender_name,
                    "SenderEmail": sender_email,
                    "Subject": subject,
                    "Date": date_received,
                    "Time": time_received,
                    "Payload": ' '.join(cleaned_payload.split()),
                    "PhoneNumber": phone_numbers
                }

                filtered_email_list.append(email_info)

            output_json = json.dumps(filtered_email_list, indent=2)

            Mail.mail_to_csv(output_json)

        except (KeyboardInterrupt, Exception, ConnectionError) as e:
            e_type, e_object, e_traceback = sys.exc_info()

            e_filename = os.path.split(e_traceback.tb_frame.f_code.co_filename)[1]
            e_message = str(e)
            e_line_number = e_traceback.tb_lineno

            error = (
                f'Exception type: {e_type}\n'
                f'Exception filename: {e_filename}\n'
                f'Exception line number: {e_line_number}\n'
                f'Exception message: {e_message}'
            )

            print(error)

        finally:
            self.mail.logout()

    @staticmethod
    def cleaning_mail(payload):
        for x in ['<h1>', '<h2>', '<h3>', '<h4>', '<h5>', '<h6>', '<p>', '<span>', '<a>']:
            if x in payload:
                soup = BeautifulSoup(payload, 'html.parser')
                main_content = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span', 'a'])

                data = ''
                for content in main_content:
                    data += content.get_text(strip=True) + ' '
                payload = data
            else:
                pass

        # Cleaning - Hyperlinks
        cleaned_payload = re.sub(r'http\S+', '', payload)
        # Cleaning - Unicode Characters
        cleaned_payload = re.sub(r'[^\x00-\x7F]+', '', cleaned_payload)
        # Cleaning - Unnecessary Punctuations
        cleaned_payload = re.sub(r'[^\w\s.,-?:;]', '', cleaned_payload)
        # Cleaning - Repeated unnecessary character
        cleaned_payload = re.sub(r'([^\w\s])\1+', r'\1', cleaned_payload)

        if cleaned_payload.isspace():
            cleaned_payload += "Blank Mail"

        return cleaned_payload

    @staticmethod
    def mail_to_csv(email_json_data):
        data_frame = pd.read_json(email_json_data)
        data_frame.to_csv('mail1.csv', index=False)

        print("Data Saved!!")


if __name__ == "__main__":
    app = Mail()
    app.mail_data()
