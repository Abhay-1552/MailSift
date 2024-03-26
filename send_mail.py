import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv


class SMTP:
    def __init__(self):
        load_dotenv('.env')

        self.smtp_server = os.getenv('SMTP_SERVER')
        self.smtp_port = int(os.getenv('SMTP_PORT'))

        self.sender_name = 'Abhay Patel'
        self.sender_email = os.getenv('MAIL')
        self.sender_password = os.getenv('PASSWORD')

        self.server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        self.server.starttls()
        self.server.login(self.sender_email, self.sender_password)

    def send_mail(self, recipient_email, subject, body):
        message = MIMEMultipart()
        message['From'] = self.sender_name
        message['To'] = recipient_email

        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        try:
            # Connect to the SMTP server
            self.server.sendmail(self.sender_email, recipient_email, message.as_string())

            # Close the connection to the SMTP server
            print('Mail sent successfully!')
            self.server.quit()
        except Exception as e:
            print(f"An error occurred while sending the email: {str(e)}")


if __name__ == '__main__':
    app = SMTP()
    email = 'popstar1552@gmail.com'
    subject = 'MailSift - Test Email'
    body = 'This is a test email sent using smtplib.'
    app.send_mail(email, subject, body)
