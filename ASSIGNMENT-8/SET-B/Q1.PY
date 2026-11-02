from flask import Flask, request
import psycopg2

app = Flask(__name__)

def db_connect():
    return psycopg2.connect(
        dbname = 'employee',
        user = 'postgres',
        password = 'joya',
        host = 'localhost',
        port = '5432'
    )

@app.route('/create_table')
def create_table():
    try:
        conn = db_connect()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS Employee(
                emp_id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                department VARCHAR(100),
                salary FLOAT
            );

        """)
        conn.commit()
        cur.close()
        conn.close()
        return "Employee table created successfully!!"

    except Exception as e:
        return f"Error : {e}"

@app.route('/insert_records')
def insert_records():
    try:

        conn = db_connect()
        cur = conn.cursor()

        employees = [
            ("Joya Patel", "IT", 45000),
            ("Vaiju Shinde", "HR", 40000),
            ("Anisha Vishwasrao", "Finance", 50000),
            ("Divya Modhave", "Marketing", 42000),
            ("Sana Ansar", "IT", 55000)
        ]

        cur.executemany("INSERT INTO Employee (name, department, salary) VALUES(%s,%s,%s);", employees)

        conn.commit()
        cur.close()
        conn.close()

        return "5 Record inserted sucessfully!!"

    except Exception as e:
        return f"Error : {e}"

@app.route('/search_employee/<int:eid>')
def search_employee(eid):

    try:

        conn = db_connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Employee WHERE emp_id = %s;",(eid,))

        employee = cur.fetchone()

        cur.close()
        conn.close()

        if employee:
            return f"Employee ID: {employee[0]}, Name: {employee[1]}, Department: {employee[2]}, Salary: {employee[3]}"
        else:
            return "Employee not found"


    except Exception as e:
        return f"Error : {e}"
if __name__ == '__main__':
    app.run(debug= True, use_reloader =False)