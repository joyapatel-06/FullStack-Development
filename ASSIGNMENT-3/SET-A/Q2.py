from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Name : Joya , Roll Number : 49"

if __name__ == "__main__":
    app.run(debug=True)