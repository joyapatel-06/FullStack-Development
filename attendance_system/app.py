
from datetime import date
from functools import wraps

import psycopg2
import psycopg2.extras
from flask import Flask, redirect, render_template, request, make_response, url_for
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from werkzeug.security import generate_password_hash, check_password_hash

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "attendance_db",
    "user": "postgres",
    "password": "joya",
}
SECRET_KEY = "change-this-secret-key"
TOKEN_MAX_AGE = 60 * 60 * 8  

app = Flask(__name__) 
serializer = URLSafeTimedSerializer(SECRET_KEY)


def db(sql, params=None, fetch=None):
    """Run one SQL query. fetch = None | 'one' | 'all'."""
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, params or ())
            result = None
            if fetch == "one":
                result = cur.fetchone()
            elif fetch == "all":
                result = cur.fetchall()
        conn.commit()
        return result
    finally:
        conn.close()


def init_db():
    """Create tables if they do not exist."""
    db("""
        CREATE TABLE IF NOT EXISTS teachers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    db("""
        CREATE TABLE IF NOT EXISTS students (
            id SERIAL PRIMARY KEY,
            roll_no VARCHAR(30) UNIQUE NOT NULL,
            name VARCHAR(100) NOT NULL,
            class_name VARCHAR(50) NOT NULL
        )
    """)
    db("""
        CREATE TABLE IF NOT EXISTS attendance (
            id SERIAL PRIMARY KEY,
            student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
            att_date DATE NOT NULL,
            status VARCHAR(10) NOT NULL CHECK (status IN ('Present', 'Absent')),
            UNIQUE (student_id, att_date)
        )
    """)


def current_teacher():
    token = request.cookies.get("auth_token")
    if not token:
        return None
    try:
        teacher_id = serializer.loads(token, max_age=TOKEN_MAX_AGE)
    except (BadSignature, SignatureExpired):
        return None
    return db("SELECT id, name FROM teachers WHERE id = %s", (teacher_id,), "one")

def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        teacher = current_teacher()
        if not teacher:
            return redirect(url_for("login"))
        request.teacher = teacher
        return view(*args, **kwargs)
    return wrapper


@app.context_processor
def inject_common():
    """Make 'teacher' and 'msg' available in every template."""
    return {
        "teacher": getattr(request, "teacher", None),
        "msg": request.args.get("msg"),
    }

@app.route("/")
def home():
    return redirect(url_for("dashboard"))


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        name = request.form["name"].strip()
        username = request.form["username"].strip()
        password = request.form["password"]
        if db("SELECT id FROM teachers WHERE username = %s", (username,), "one"):
            error = "Username already taken."
        else:
            db(
                "INSERT INTO teachers (name, username, password_hash) VALUES (%s, %s, %s)",
                (name, username, generate_password_hash(password)),
            )
            return redirect(url_for("login", msg="Account created. Please login."))
    return render_template("register.html", error=error)


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        user = db(
            "SELECT id, password_hash FROM teachers WHERE username = %s",
            (request.form["username"].strip(),),
            "one",
        )
        if user and check_password_hash(user["password_hash"], request.form["password"]):
            resp = make_response(redirect(url_for("dashboard")))
            resp.set_cookie(
                "auth_token", serializer.dumps(user["id"]),
                max_age=TOKEN_MAX_AGE, httponly=True, samesite="Lax",
            )
            return resp
        error = "Wrong username or password."
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    resp = make_response(redirect(url_for("login", msg="Logged out.")))
    resp.delete_cookie("auth_token")
    return resp


@app.route("/dashboard")
@login_required
def dashboard():
    total_students = db("SELECT COUNT(*) AS c FROM students", fetch="one")["c"]
    today_rows = db(
        "SELECT status, COUNT(*) AS c FROM attendance WHERE att_date = %s GROUP BY status",
        (date.today(),), "all",
    )
    counts = {r["status"]: r["c"] for r in today_rows}
    overall_row = db(
        "SELECT COUNT(*) AS total, COUNT(*) FILTER (WHERE status = 'Present') AS present FROM attendance",
        fetch="one",
    )
    overall = round(overall_row["present"] * 100 / overall_row["total"], 1) if overall_row["total"] else 0
    return render_template(
        "dashboard.html",
        total_students=total_students,
        present_today=counts.get("Present", 0),
        absent_today=counts.get("Absent", 0),
        overall=overall,
    )


@app.route("/students", methods=["GET", "POST"])
@login_required
def students():
    error = None
    if request.method == "POST":
        roll_no = request.form["roll_no"].strip()
        if db("SELECT id FROM students WHERE roll_no = %s", (roll_no,), "one"):
            error = "That roll number already exists."
        else:
            db(
                "INSERT INTO students (roll_no, name, class_name) VALUES (%s, %s, %s)",
                (roll_no, request.form["name"].strip(), request.form["class_name"].strip()),
            )
            return redirect(url_for("students", msg="Student added."))
    rows = db("SELECT * FROM students ORDER BY class_name, roll_no", fetch="all")
    return render_template("students.html", students=rows, error=error)


@app.route("/students/delete/<int:student_id>", methods=["POST"])
@login_required
def delete_student(student_id):
    db("DELETE FROM students WHERE id = %s", (student_id,))
    return redirect(url_for("students", msg="Student deleted."))


@app.route("/attendance", methods=["GET", "POST"])
@login_required
def attendance():
    today = date.today().isoformat()

    if request.method == "POST":
        att_date = request.form["att_date"]
        for s in db("SELECT id FROM students", fetch="all"):
            status = request.form.get(f"status_{s['id']}", "Present")
            db(
                """INSERT INTO attendance (student_id, att_date, status)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (student_id, att_date) DO UPDATE SET status = EXCLUDED.status""",
                (s["id"], att_date, status),
            )
        return redirect(url_for("attendance", att_date=att_date, msg="Attendance saved."))

    att_date = request.args.get("att_date", today)
    rows = db(
        """SELECT s.id, s.roll_no, s.name, s.class_name, a.status
            FROM students s
            LEFT JOIN attendance a ON a.student_id = s.id AND a.att_date = %s
            ORDER BY s.class_name, s.roll_no""",
        (att_date,), "all",
    )
    return render_template("attendance.html", students=rows, att_date=att_date, today=today)


@app.route("/report")
@login_required
def report():
    rows = db(
        """SELECT s.roll_no, s.name, s.class_name,
            COUNT(a.id) AS total,
            COUNT(a.id) FILTER (WHERE a.status = 'Present') AS present
        FROM students s
        LEFT JOIN attendance a ON a.student_id = s.id
        GROUP BY s.id
        ORDER BY s.class_name, s.roll_no""",
        fetch="all",
    )
    for r in rows:
        r["percent"] = round(r["present"] * 100 / r["total"], 1) if r["total"] else 0
    return render_template("report.html", rows=rows)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
