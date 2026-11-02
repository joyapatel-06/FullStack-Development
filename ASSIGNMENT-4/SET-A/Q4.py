from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Welcome to the Home Page</h1>"

@app.route('/student')
def student():
    return "<h1>This is the Student Page.</h1>"

@app.route('/faculty')
def faculty():
    return "<h1>Welcome to the Faculty Page</h1>"

if __name__ == '__main__':
    app.run(debug=True)