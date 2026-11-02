from flask import Flask, request
import psycopg2

app = Flask(__name__)

def db_connect():
    return psycopg2.connect(
        dbname = 'Hospital',
        user = 'postgres',
        password = "root",
        host = "localhost",
        port = "5432"
    )

@app.route('/create_table')
def create_table():
    try:
        conn = db_connect()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Patient(
            patient_id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            age INT,
            disease VARCHAR(100)
            );
        
        """)

        conn.commit()
        cur.close()
        conn.close()
        return "Patient Table Created Successfully!"

    except Exception as e:
        return f"Error : {e}"

@app.route('/insert_records')
def insert_patients():
    try:
        conn = db_connect()
        cur = conn.cursor()
        patients = [
            ('Joya',19,'Fever'),
            ('Anisha', 20,'Diabetes'),
            ('Vaiju', 19, 'Fever'),
            ('Akshada', 20, 'Diabetes'),
            ('Sana', 20, 'Fever')
        ]

        cur.executemany("INSERT INTO Patient(name,age,disease) VALUES(%s,%s,%s)",patients)
        conn.commit()
        cur.close()
        conn.close()

        return "5 record inserted sucessfully!"

    except Exception as e:
        return f"Error: {e}"

@app.route('/search_patient/<int:pid>')
def search_patient(pid):
    try:
        conn = db_connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Patient WHERE patient_id = %s;",(pid,))
        patient = cur.fetchone()

        cur.close()
        conn.close()

        if patient:
            return f"Patient Details : ID={patient[0]}, Name={patient[1]}, Age={patient[2]}, Disease={patient[3]}"
        else:
            return "No patient associated with that ID"

    except Exception as e:
        return f"Error : {e}"
if __name__ == '__main__':
    app.run(debug=True)