import os
from flask import Flask, render_template, request, session, redirect
from login import MongoDB
from mails import MAIL
from send_mail import SMTP
from visuals import Graph

app = Flask(__name__, template_folder="templates")

# For Sessions
app.secret_key = os.urandom(32)

# Creating folder for attachments
UPLOAD_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads", "MailSift")

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if os.path.exists(app.config['UPLOAD_FOLDER']):
    print(f"Upload folder exists at {app.config['UPLOAD_FOLDER']}")
else:
    try:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        print(f"Upload folder created at {app.config['UPLOAD_FOLDER']}")
    except OSError as e:
        print(f"Error creating upload folder: {e}")

os.chmod(UPLOAD_FOLDER, 0o744)

# Database connectivity
mongo = MongoDB()

# SMTP connectivity
smtp = SMTP()

# Define json_mail_data globally
json_mail_data = None


@app.route('/')
def index():
    message = session.pop('response', None)

    return render_template('login.html', popup=message is not None, message=message)


@app.route('/home')
def home():
    username = session.get('name')
    email = session.get('email')
    visible: bool = False

    if json_mail_data:
        visible: bool = True

    return render_template('home.html', name=username, email=email, visible=visible)


@app.route('/dashboard')
def dashboard():
    data = json_mail_data

    graph = Graph(data)

    cloud_text = graph.word_cloud()
    sender_data = graph.sender_count_to_lists()
    date_count = graph.date_count_function()
    time_quarter = graph.mails_per_time_intervals()

    return render_template('dashboard.html', cloud_text=cloud_text, sender_data=sender_data,
                           date_count=date_count, time_quarter=time_quarter)


@app.route('/mail')
def mail():
    json_data = json_mail_data
    alert_msg = session.get('alert_msg')

    if alert_msg is not None:
        return render_template('mails.html', json_data=json_data, alert_msg=alert_msg)
    else:
        return render_template('mails.html', json_data=json_data)


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('loginEmail')
        password = request.form.get('loginPassword')

        user_login = mongo.check_user(email, password)

        if user_login[0]:
            session['user_session'] = email

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


@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('user_session', None)
    session.pop('name', None)
    session.pop('email', None)
    return redirect('/')


@app.route('/date_input', methods=['POST'])
def date_input():
    global json_mail_data

    if request.method == 'POST':
        month = request.form.get('month')
        year = request.form.get('year')

        # Mail connectivity
        inbox = MAIL()
        json_mail_data = inbox.inbox_mails(month, year)

    return redirect('/home')


@app.route('/send_mail', methods=['POST'])
def send_mail():
    if request.method == 'POST':
        reply = request.form.get('mailReply')
        attachment_files = request.files.getlist('fileAttachment')

        reply_text = f'Reply: {reply}'
        attachments = []

        if attachment_files:
            for file in attachment_files:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)
                attachments.append(file_path)
        else:
            attachments = None

        # Send email
        email = 'popstar1552@gmail.com'
        title = 'MailSift - Test Email'

        smtp.send_mail(email, title, reply_text, attachments)

        msg = "Process completed successfully!"
        session['alert_msg'] = msg

        return redirect('/mail')
    else:
        msg = "Error occurs! Try Again"
        session['alert_msg'] = msg

        return redirect('/mail')


if __name__ == '__main__':
    app.run(port=8000, debug=True, use_reloader=False)
