from flask import Flask

app = Flask(__name__)

@app.route('/employee/<name>')
def employee(name):
    return f"<h1>Welcome, {name}!</h1><p>We are glad to have you in our organization.</p>"

if __name__ == '__main__':
    app.run(debug=True)