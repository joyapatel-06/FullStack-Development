from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']

        if username == "admin":
            return "Login Successful"
        else:
            return "Invalid Username"

    return '''
    <form method="post">
        Username:
        <input type="text" name="username"><br>
        <input type="submit" value="Login">
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)