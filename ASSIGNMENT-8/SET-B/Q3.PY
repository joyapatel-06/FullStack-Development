from flask import Flask
import psycopg2

app = Flask(__name__)

def db_connect():
    conn = psycopg2.connect(
        dbname = 'hospital',
        user = 'postgres',
        password = 'joya',
        host = 'localhost',
        port = '5432'    
    )

    return conn
@app.route('/create_table')
def table_create():

    try:

        conn = db_connect()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS Patient1(
                pid serial PRIMARY KEY,
                name VARCHAR(100),
                age INT
            );
        """)

        conn.commit()
        cur.close()
        conn.close()
        return "Table created sucessfully"
    
    except Exception as e:
        return f"Error :{e}"

@app.route('/insert_record')
def insert_record():

    try:

        conn = db_connect()
        cur = conn.cursor()

        patients = [
                    ("Joya", 19 ),
                    ("Vaiju", 19 ),
                    ("Anisha", 20 ),
                    ("Sana", 20 ),
                    ("Divya", 20)
                ]

        cur.executemany("INSERT INTO Patient1(name, age) VALUES (%s,%s);",patients)

        conn.commit()
        cur.close()
        conn.close()

        return "record inserted sucessfully"

    except Exception as e:
        return f"Error :{e}"

if __name__ == '__main__':
    app.run(debug=True)