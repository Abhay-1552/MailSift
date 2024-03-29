from flask import Flask, render_template, request, session, redirect
from login import MongoDB
from send_mail import SMTP
import os
import sys
import stat
import random
import string

app = Flask(__name__, template_folder="template")

# For Sessions
characters = string.ascii_letters + string.digits + string.punctuation
random_string = ''.join(random.choice(characters) for _ in range(20))

app.secret_key = random_string

# Database connectivity
mongo = MongoDB()

# SMTP connectivity
smtp = SMTP()


@app.route('/')
def index():
    message = session.pop('response', None)

    return render_template('login.html', popup=message is not None, message=message)


@app.route('/home')
def home():
    username = session.get('name')
    email = session.get('email')

    return render_template('home.html', name=username, email=email)


@app.route('/mail')
def mail():
    return render_template('mails.html')


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('loginEmail')
        password = request.form.get('loginPassword')

        user_login = mongo.check_user(email, password)

        if user_login[0]:
            session['name'] = user_login[0]
            session['email'] = user_login[1]

            return redirect('/home')

    session['response'] = "Invalid Credentials!"
    return redirect('/')


@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('signupName')
        email = request.form.get('signupEmail')
        passkey = request.form.get('signupPasskey')
        password = request.form.get('signupPassword')

        message = mongo.insert_data(name, email, passkey, password)
        session['response'] = message

    return redirect('/')


@app.route('/send_mail', methods=['POST'])
def send_mail():
    if request.method == 'POST':
        reply = request.form.get('mailReply')
        attachment_files = request.files.getlist('fileAttachment')

        reply_text = f'Reply: {reply}'
        attachments = []

        if attachment_files:
            for file in attachment_files:
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                attachments.append(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        print(attachments)
        print(reply_text)

        # Send email
        email = 'popstar1552@gmail.com'  # Replace with recipient email address
        title = 'MailSift - Test Email'

        smtp.send_mail(email, title, reply_text, attachments)

        # Return a response to the user
        return "Form submitted successfully. Email sent."
    else:
        return "Method not allowed."


if __name__ == '__main__':
    UPLOAD_FOLDER = os.path.expanduser("~/Downloads/MailSift/")

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.chmod(UPLOAD_FOLDER, stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    if os.path.exists(app.config['UPLOAD_FOLDER']):
        print(f"Upload folder exists at {app.config['UPLOAD_FOLDER']}")
    else:
        try:
            os.makedirs(app.config['UPLOAD_FOLDER'])
            print(f"Upload folder created at {app.config['UPLOAD_FOLDER']}")
        except OSError as e:
            print(f"Error creating upload folder: {e}")

    app.run(port=8000, debug=True)
