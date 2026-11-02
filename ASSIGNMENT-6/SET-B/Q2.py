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

    employee_details = ""

    for name, department, salary in employees:
        employee_details += f"""
        <p>
            Name: {name}<br>
            Department: {department}<br>
            Salary: ₹{salary}
        </p>
        <hr>
        """

    return f"""
    <h2>List of Employees</h2>
    {employee_details}
    """

if __name__ == "__main__":
    app.run(debug=True)