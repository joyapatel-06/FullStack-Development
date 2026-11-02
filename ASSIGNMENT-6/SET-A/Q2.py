from flask import Flask

app = Flask(__name__)

@app.route('/')
def students():
    names = ["Joya", "Vaiju", "Anisha", "Divya", "Sana"]

    # Corrected: use names instead of students
    student_names = "<br>".join(names)

    return f"""
    <h2>List of Students</h2>
    {student_names}
    """

if __name__ == "__main__":
    app.run(debug=True)