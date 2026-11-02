from flask import Flask

app = Flask(__name__)

@app.route('/Contact')
def Contact():
    return "<h1>This is the Contact Page</h1>"

@app.route('/Services')
def Services():
    return "<h1>This is the services page</h1>"

if __name__ == '__main__':
    app.run(debug=True)