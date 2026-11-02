from flask import Flask

app = Flask(__name__)

@app.route("/")
def employee_list():

    employees = [
        ("Joya Patel", "IT", 40000),
        ("Vaiju Shinde", "HR", 40000),
        ("Anisha Vishwashrao", "Finance", 50000),
        ("Sana Ansar", "Marketing", 42000),
        ("Vedant Shinde", "IT", 55000)
    ]
    result = "<h2>Employee Details</h2>"

    for name, department, salary in employees:
        result += f"""
            Name  : {name}<br>
            Department : {department}<br>
            Salary : ₹{salary}<br><br>
        """
    return result

if __name__ == "__main__":
    app.run(debug=True)