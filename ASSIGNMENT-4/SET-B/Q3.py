from flask import Flask

app = Flask(__name__)

@app.route('/employee')
def employee():
    return "<h1>Employee Page</h1><p>Welcome to the Employee Section.</p>"

@app.route('/department')
def department():
    return "<h1>Department Page</h1><p>Welcome to the Department Section.</p>"

@app.route('/contact')
def contact():
    return "<h1>Contact Page</h1><p>Contact us at: pjoya158@gmail.com</p>"

if __name__ == '__main__':
    app.run(debug=True)