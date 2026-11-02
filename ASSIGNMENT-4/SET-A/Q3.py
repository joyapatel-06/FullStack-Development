from flask import Flask

app = Flask(__name__)

@app.route('/course/<string:name>')
def Course_info (name):
    return f"""
    <P>{name}</P>
    <p>"Welcome to the Course!"</p>
    """

if __name__ == '__main__':
    app.run(debug=True)