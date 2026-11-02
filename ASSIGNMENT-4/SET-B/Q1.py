from flask import Flask

app = Flask(__name__)

@app.route('/student/<name>')
def student(name):
    return f"<h1>Student Name: {name.title()}</h1>"

if __name__ == '__main__':
    app.run(debug=True)