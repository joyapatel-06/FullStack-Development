from flask import Flask
import psycopg2

app = Flask(__name__)

@app.route('/connect')
def connect_db():
    try:
        conn = psycopg2.connect(
            dbname="student",
            user="postgres",
            password="joya",
            host="localhost",
            port="5432"
        )
        conn.close()
        return "Database Connected Successfully"
    except Exception as e:
        return f"Error: {e}"

@app.route('/create_table')
def create_table():
    try:
        conn = psycopg2.connect(
            dbname="student",
            user="postgres",
            password="joya",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Student (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                age INT,
                course VARCHAR(50)
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
        return "Student Table Created Successfully"
    except Exception as e:
        return f"Error: {e}"

@app.route('/insert')
def insert_students():
    try:
        conn = psycopg2.connect(
            dbname="student",
            user="postgres",
            password="joya",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()
        students = [
            ('Joya',19,'Information Technology'),
            ('Anisha', 20, 'Information Technology'),
            ('Vaiju', 19, 'Information Technology'),
            ('Akshada', 20, 'Information Technology'),
            ('Sana', 20, 'Cyber Security')
        ]
        cur.executemany("INSERT INTO Student (name, age, course) VALUES (%s, %s, %s);", students)
        conn.commit()
        cur.close()
        conn.close()
        return "5 Student Records Inserted Successfully"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    app.run(debug=True)