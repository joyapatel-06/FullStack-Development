from flask import Flask

app = Flask(__name__)

@app.route('/square/<int:num>')
def square(num):
    return f"Number: {num}<br>Square: {num * num}"

if __name__ == '__main__':
    app.run(debug=True)