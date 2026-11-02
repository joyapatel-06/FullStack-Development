from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return '''
        <h2>Login Form</h2>
        <form method="POST" action="/login">
            Username: <input type="text" name="username"><br><br>
            Password: <input type="password" name="password"><br><br>
            <input type="submit" value="Login">
        </form>
    '''

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    return "Username: " + username + "<br>Password: " + password

if __name__ == '__main__':
    app.run(debug=True)