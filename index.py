from flask import Flask, render_template, request, jsonify
import visuals

app = Flask(__name__, template_folder="template")


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('loginEmail')
        password = request.form.get('loginPassword')
        # Here you can process the login data, like checking against a database
        return f"Login: Email - {email}, Password - {password}"


@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('signupName')
        email = request.form.get('signupEmail')
        passkey = request.form.get('signupPasskey')
        password = request.form.get('signupPassword')
        # Here you can process the signup data, like storing in a database
        return f"Signup: Name - {name}, Email - {email}, Passkey - {passkey}, Password - {password}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
