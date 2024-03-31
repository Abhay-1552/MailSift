import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import mimetypes
from dotenv import load_dotenv


class SMTP:
    def __init__(self):
        load_dotenv('.env')

        self.smtp_server = os.getenv('SMTP_SERVER')
        self.smtp_port = int(os.getenv('SMTP_PORT'))

        self.sender_name = 'Abhay Patel'
        self.sender_email = os.getenv('MAIL')
        self.sender_password = os.getenv('PASSKEY')

        self.server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        self.server.starttls()
        self.server.login(self.sender_email, self.sender_password)

    def send_mail(self, recipient_email, subject, body, attachment_paths=None):
        message = MIMEMultipart()

        message['From'] = self.sender_name
        message['To'] = recipient_email
        message['Subject'] = subject

        # Attach body
        message.attach(MIMEText(body, 'plain'))

        # Attach files if provided
        if attachment_paths:
            for attachment_path in attachment_paths:
                content_type, _ = mimetypes.guess_type(attachment_path)
                main_type, sub_type = content_type.split('/', 1)

                with open(attachment_path, 'rb') as attachment_file:
                    part = MIMEBase(main_type, sub_type)
                    part.set_payload(attachment_file.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(attachment_path)}"')
                    message.attach(part)

        try:
            # Connect to the SMTP server
            self.server.sendmail(self.sender_email, recipient_email, message.as_string())

            # Close the connection to the SMTP server
            print('Mail sent successfully!')
            self.server.quit()
        except Exception as e:
            print(f"An error occurred while sending the email: {str(e)}")

