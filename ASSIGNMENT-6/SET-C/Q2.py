from flask import Flask

app = Flask(__name__)

@app.route("/students")
def students():

    students = [
        ("Joya", 85),
        ("Vaiju", 45),
        ("Anisha", 75),
        ("Sana", 55),
        ("Vedant", 95)
    ]

    result = "<h2>Students Scorign more than 60 Marks</h2>"

    for name, marks in students:
        if marks >= 60:
            result += f"{name} - {marks} marks <br>"

    return result

if __name__ == "__main__":
    app.run(debug=True)
    


            