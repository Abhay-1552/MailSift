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


class Mail:
    def __init__(self):
        load_dotenv(".env")

        self.email_address = os.getenv('MAIL')
        self.email_password = os.getenv('PASSWORD')
        self.imap_server = os.getenv('SERVER')
        self.imap_port = int(os.getenv('PORT'))

        self.mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
        self.mail.login(self.email_address, self.email_password)

    def mail_data(self):
        try:
            self.mail.select("inbox")

            # Search for the latest 10 emails in the mailbox
            status, messages = self.mail.search(None, "ALL")
            messages = messages[0].split()
            messages.reverse()
            top_messages = messages[:20]

            filtered_email_list = []

            # Fetch and process each email
            for email_id in top_messages:
                status, msg_data = self.mail.fetch(email_id, "(RFC822)")

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

                payload = email_message.get_payload()
                decoded_payload = ''

                # Get the body of the email
                if email_message.is_multipart():
                    for part in payload:
                        if part.get_content_type() == "text/plain":
                            decoded_payload = part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8", errors="ignore")
                            break
                        elif part.get_content_type() == "text/html":
                            html_payload = part.get_payload()
                            soup = BeautifulSoup(html_payload, 'html.parser')
                            decoded_payload = soup.get_text()
                elif email_message.get_content_type() == "text/plain":
                    decoded_payload = payload.decode(email_message.get_content_charset() or "utf-8", errors="ignore")

                # Clean URLs from the payload
                cleaned_payload = re.sub(r'http\S+', '', decoded_payload)

                email_info = {
                    "SenderName": sender_name,
                    "SenderEmail": sender_email,
                    "Subject": subject,
                    "Date": date_received,
                    "Time": time_received,
                    "Payload": ' '.join(cleaned_payload.split())
                }

                print(email_info)
                print('-' * 200)

                # Add the dictionary to the list
                filtered_email_list.append(email_info)

            # Output the filtered information in JSON format
            output_json = json.dumps(filtered_email_list, indent=2)
            print(output_json)

            Mail.mail_to_excel(output_json)

        finally:
            # Logout from the server
            self.mail.logout()

    @staticmethod
    def mail_to_excel(email_json_data):
        data_frame = pd.read_json(email_json_data)
        data_frame.to_excel("mail.xlsx")

        print("Data Saved!!")


if __name__ == "__main__":
    app = Mail()
    app.mail_data()
