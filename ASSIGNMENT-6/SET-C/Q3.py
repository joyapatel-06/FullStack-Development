from flask import Flask, render_template

app = Flask(__name__)

students = {
    "Joya": [85, 45, 87],
    "Vaiju": [45, 55, 65],
    "Anisha": [56, 78, 67],
    "Sana": [78, 98, 67]
}

@app.route('/')
def display_marks():
    results = []

    for name, marks in students.items():
        total = sum(marks)
        average = total / len(marks)
        highest = max(marks)
        lowest = min(marks)

        results.append({
            "name": name,
            "marks": marks,
            "total": total,
            "average": average,
            "highest": highest,
            "lowest": lowest
        })

    return render_template("student.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)
