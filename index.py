from flask import Flask, render_template, request, session, redirect, jsonify
from login import MongoDB
from send_mail import SMTP
import os
import random
import string

app = Flask(__name__, template_folder="template")

# For Sessions
characters = string.ascii_letters + string.digits + string.punctuation
random_string = ''.join(random.choice(characters) for _ in range(20))

app.secret_key = random_string

# Creating folder for attachments
UPLOAD_FOLDER = os.path.expanduser("~\\Downloads\\MailSift")

os.chmod(UPLOAD_FOLDER, 0o744)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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


@app.route('/date_input', methods=['POST'])
def date_input():
    if request.method == 'POST':
        date1 = request.form.get('monthYear')

        print(date1)
    return '', 204


@app.route('/send_mail', methods=['POST'])
def send_mail():
    if request.method == 'POST':
        reply = request.form.get('mailReply')
        attachment_files = request.files.getlist('fileAttachment')

        reply_text = f'Reply: {reply}'
        attachments = []

        if os.path.exists(app.config['UPLOAD_FOLDER']):
            print(f"Upload folder exists at {app.config['UPLOAD_FOLDER']}")
        else:
            try:
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                print(f"Upload folder created at {app.config['UPLOAD_FOLDER']}")
            except OSError as e:
                print(f"Error creating upload folder: {e}")

        if attachment_files:
            for file in attachment_files:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)
                attachments.append(file_path)
        else:
            attachments = None

        # Send email
        email = 'popstar1552@gmail.com'  # Replace with recipient email address
        title = 'MailSift - Test Email'

        smtp.send_mail(email, title, reply_text, attachments)

        # Return a response to the user
        return "alert('Process completed successfully!');"
    else:
        return "alert('Error occurs! Try Again');"


if __name__ == '__main__':
    app.run(port=8000, debug=True)
