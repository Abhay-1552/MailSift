from flask import Flask, render_template, request, redirect, url_for, session
from login import MongoDB
import random
import string

app = Flask(__name__, template_folder="template")

characters = string.ascii_letters + string.digits + string.punctuation
random_string = ''.join(random.choice(characters) for _ in range(20))

app.secret_key = random_string

mongo = MongoDB()


@app.route('/')
def index():
    message = session.get('response')

    if message:
        return render_template('login.html', popup=True, message=message)
    else:
        return render_template('login.html', popup=False)


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

            return redirect(url_for('home', name=user_login[0], email=user_login[1]))
        else:
            message = "Invalid Credentials!"
            session['response'] = message

            return redirect(url_for('index', message=message))


@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('signupName')
        email = request.form.get('signupEmail')
        passkey = request.form.get('signupPasskey')
        password = request.form.get('signupPassword')

        message = mongo.insert_data(name, email, passkey, password)
        session['response'] = message

        return redirect(url_for('index', message=message))


if __name__ == '__main__':
    app.run(port=8000, debug=True)
