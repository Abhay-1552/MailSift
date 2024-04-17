import imaplib
import email
import os
import re
from dotenv import load_dotenv
from dateutil import parser as date_parser
from tqdm import tqdm
import sys
from datetime import datetime
import json


class MAIL:
    def __init__(self):
        load_dotenv('.env')

        # IMAP server settings
        imap_server = os.getenv('IMAP_SERVER')
        mail_id = os.getenv('MAIL')
        password = os.getenv('PASSKEY')

        # Connect to the IMAP server
        self.mail = imaplib.IMAP4_SSL(imap_server)

        # Login to your account
        self.mail.login(mail_id, password)

        self.emails = []

    def inbox_mails(self, month, year):
        try:
            # Select the mailbox (in this case, the "INBOX")
            self.mail.select('inbox')

            month = int(month)
            year = int(year)

            start_date = datetime(year, month, 1)

            if month == 12:
                end_date = datetime(year + 1, 1, 1)
            else:
                end_date = datetime(year, month + 1, 1)

            # Format the dates in the required IMAP format
            start_date_str = start_date.strftime("%d-%b-%Y")
            end_date_str = end_date.strftime("%d-%b-%Y")

            # Construct the IMAP search query
            search_query = f'(SINCE "{start_date_str}") (BEFORE "{end_date_str}")'

            # Search for all emails in the "Primary" folder
            result, data = self.mail.search(None, search_query)

            if result == 'OK':
                for num in tqdm(data[0].split()):
                    result, data = self.mail.fetch(num, '(RFC822)')

                    if result == 'OK':
                        email_message = email.message_from_bytes(data[0][1])
                        date_string = email_message['Date']

                        parsed_date = date_parser.parse(date_string)

                        sender = email.utils.parseaddr(email_message['From'])
                        sender_name, sender_email = sender

                        email_data = {
                            'SenderName': sender_name,
                            'SenderEmail': sender_email,
                            'Subject': email_message['Subject'],
                            'Date': parsed_date.strftime('%d/%m/%Y'),
                            'Time': parsed_date.strftime('%H:%M'),
                            'Attachments': [],
                        }

                        # Iterate over each part of the email (plaintext or multipart)
                        for part in email_message.walk():
                            content_type = part.get_content_type()

                            if content_type == 'text/plain':
                                email_body = part.get_payload(decode=True).decode(part.get_content_charset())

                                email_body = (f"<p>{email_body}</p>".replace('\r', '')
                                              .replace('\n', '</p><p>').replace('<p></p>', ''))

                                email_body = (re.sub(r'<(https:[^>]+)>', r"<a href='\1'>Click Here</a>", email_body)
                                              .replace(r'(https?://\S+)', r"<a href='\1'>Click Here</a>"))

                                email_data['Body'] = email_body

                            else:
                                filename = part.get_filename()
                                if filename:
                                    email_data['Attachments'].append({'Filename': filename, 'Type': content_type})

                        self.emails.append(email_data)

            # return self.to_json()
            return self.emails

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

    # def to_json(self):
    #     # Convert data to JSON format
    #     json_data = json.dumps(self.emails)
    #
    #     return json_data


# if __name__ == '__main__':
#     app = MAIL()
#
#     mail_data = app.inbox_mails()
#     print(mail_data)
