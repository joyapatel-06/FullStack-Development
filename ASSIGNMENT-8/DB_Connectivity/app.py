from flask import Flask
import psycopg2
app=Flask(__name__)

def db_connect():
    conn=psycopg2.connect(
        dbname='hospital',
        user='postgres',
        password='joya',
        host='localhost',
        port=5432
    )
    return conn
@app.route('/create_table')
def create_table():
    try:
        conn=db_connect()
        cur=conn.cursor()

        cur.execute("""create table if not exists hospital(
        id serial primary key,
        hname varchar(100),
        department varchar(100));
        """)
        conn.commit()
        cur.close()
        conn.close()
        return "table create successfully !"
    
    except Exception as e:
        return "error :{e}"

if __name__=='__main__':
    app.run(debug=True)

