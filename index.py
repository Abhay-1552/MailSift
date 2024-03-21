from flask import Flask, render_template, request, redirect, url_for
from login import MongoDB

app = Flask(__name__, template_folder="template")

mongo = MongoDB()


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/mail')
def mail():
    return render_template('mails.html')


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('loginEmail')
        password = request.form.get('loginPassword')

        user_login = mongo.check_user(email, password)

        if user_login:
            return redirect(url_for('home'))
        else:
            return redirect(url_for('index'))


@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('signupName')
        email = request.form.get('signupEmail')
        passkey = request.form.get('signupPasskey')
        password = request.form.get('signupPassword')

        mongo.insert_data(name, email, passkey, password)

        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=8000, debug=True)
