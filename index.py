from flask import Flask, render_template, request, jsonify
import visuals
from login import MongoDB


app = Flask(__name__, template_folder="template")

mongo = MongoDB()


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('loginEmail')
        password = request.form.get('loginPassword')
        # Here you can process the login data, like checking against a database

        user_login = mongo.check_user(email, password)

        if user_login:
            return "Valid user"
        else:
            return "Unregistered"


@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('signupName')
        email = request.form.get('signupEmail')
        passkey = request.form.get('signupPasskey')
        password = request.form.get('signupPassword')

        user_signup = mongo.insert_data(name, email, passkey, password)

        return user_signup


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
