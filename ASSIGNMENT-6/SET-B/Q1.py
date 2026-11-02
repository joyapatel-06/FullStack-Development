from flask import Flask

app = Flask(__name__)

@app.route('/')
def student():
    s = {
        "Name": "Vaiju",
        "Roll": 64,
        "Class": "TYBSc IT"
    }

    return f"""
    <h2>Student Information</h2>
    Name: {s['Name']}<br>
    Roll No: {s['Roll']}<br>
    Class: {s['Class']}
    """

if __name__ == '__main__':
    app.run(debug=True)

