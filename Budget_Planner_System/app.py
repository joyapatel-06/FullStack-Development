from flask import Flask, request, render_template, redirect, make_response
import psycopg2

app = Flask(__name__)

def db_connect():
    return psycopg2.connect(
        dbname="budget_planner",
        user="postgres",
        password="joya",
        host="localhost",
        port="5432"
    )

# Create Database Tables
def create_table():
    con = db_connect()
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            User_ID SERIAL PRIMARY KEY,
            Name VARCHAR(100),
            Email VARCHAR(100) UNIQUE,
            Password VARCHAR(100)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Transactions (
            Transaction_ID SERIAL PRIMARY KEY,
            User_ID INTEGER REFERENCES Users(User_ID),
            Transaction_Type VARCHAR(20),
            Category VARCHAR(100),
            Amount NUMERIC(10,2),
            Transaction_Date DATE,
            Description VARCHAR(200)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Budgets (
            Budget_ID SERIAL PRIMARY KEY,
            User_ID INTEGER REFERENCES Users(User_ID),
            Budget_Month INTEGER,
            Budget_Year INTEGER,
            Amount NUMERIC(10,2),
            UNIQUE(User_ID, Budget_Month, Budget_Year)
        )
    """)

    con.commit()
    cur.close()
    con.close()

def get_user_id():
    return request.cookies.get("budget_user_id")


# Home Page
@app.route("/")
def home():
    if get_user_id():
        return redirect("/dashboard")
    return render_template("index.html")


# User Registration
@app.route("/register", methods=["GET", "POST"])
def register():
    msg = ""

    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip()
        password = request.form["password"].strip()

        if name == "" or email == "" or password == "":
            msg = "Please fill in all fields."
        else:
            con = db_connect()
            cur = con.cursor()

            cur.execute("SELECT * FROM Users WHERE Email=%s", (email,))
            old_user = cur.fetchone()

            if old_user:
                msg = "Email is already registered."
            else:
                cur.execute(
                    "INSERT INTO Users (Name, Email, Password) VALUES (%s, %s, %s)",
                    (name, email, password)
                )
                con.commit()
                msg = "Registration successful. Please login."

            cur.close()
            con.close()

    return render_template("register.html", msg=msg)


# User Login
@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ""

    if request.method == "POST":
        email = request.form["email"].strip()
        password = request.form["password"].strip()

        con = db_connect()
        cur = con.cursor()

        cur.execute(
            "SELECT User_ID FROM Users WHERE Email=%s AND Password=%s",
            (email, password)
        )
        user = cur.fetchone()

        cur.close()
        con.close()

        if user:
            response = make_response(redirect("/dashboard"))
            response.set_cookie("budget_user_id", str(user[0]))
            return response
        else:
            msg = "Invalid email or password."

    return render_template("login.html", msg=msg)


# Dashboard
@app.route("/dashboard")
def dashboard():
    user_id = get_user_id()

    if not user_id:
        return redirect("/login")

    con = db_connect()
    cur = con.cursor()

    cur.execute("SELECT Name FROM Users WHERE User_ID=%s", (user_id,))
    user = cur.fetchone()

    if not user:
        cur.close()
        con.close()
        return redirect("/login")

    cur.execute("""
        SELECT
            COALESCE(SUM(CASE WHEN Transaction_Type='Income' THEN Amount ELSE 0 END), 0),
            COALESCE(SUM(CASE WHEN Transaction_Type='Expense' THEN Amount ELSE 0 END), 0)
        FROM Transactions
        WHERE User_ID=%s
        AND EXTRACT(MONTH FROM Transaction_Date)=EXTRACT(MONTH FROM CURRENT_DATE)
        AND EXTRACT(YEAR FROM Transaction_Date)=EXTRACT(YEAR FROM CURRENT_DATE)
    """, (user_id,))
    totals = cur.fetchone()

    cur.execute("""
        SELECT Transaction_Type, Category, Amount, Transaction_Date
        FROM Transactions
        WHERE User_ID=%s
        ORDER BY Transaction_Date DESC, Transaction_ID DESC
        LIMIT 5
    """, (user_id,))
    recent = cur.fetchall()

    cur.close()
    con.close()

    income = totals[0]
    expense = totals[1]
    balance = income - expense

    return render_template(
        "dashboard.html", name=user[0], income=income,
        expense=expense, balance=balance, recent=recent
    )


# Add Income or Expense
@app.route("/add_transaction", methods=["GET", "POST"])
def add_transaction():
    user_id = get_user_id()

    if not user_id:
        return redirect("/login")

    msg = ""

    if request.method == "POST":
        transaction_type = request.form["transaction_type"]
        category = request.form["category"].strip()
        amount = request.form["amount"].strip()
        transaction_date = request.form["transaction_date"]
        description = request.form["description"].strip()

        if transaction_type == "" or category == "" or amount == "" or transaction_date == "":
            msg = "Please fill in all required fields."
        else:
            try:
                amount = float(amount)
                if amount <= 0:
                    msg = "Amount must be greater than zero."
                else:
                    con = db_connect()
                    cur = con.cursor()

                    cur.execute("""
                        INSERT INTO Transactions
                        (User_ID, Transaction_Type, Category, Amount, Transaction_Date, Description)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (user_id, transaction_type, category, amount, transaction_date, description))

                    con.commit()
                    cur.close()
                    con.close()
                    return redirect("/transactions")
            except ValueError:
                msg = "Please enter a valid amount."

    return render_template("add_transaction.html", msg=msg)


# Display Transactions
@app.route("/transactions")
def transactions():
    user_id = get_user_id()

    if not user_id:
        return redirect("/login")

    con = db_connect()
    cur = con.cursor()

    cur.execute("""
        SELECT Transaction_ID, Transaction_Type, Category, Amount,
            Transaction_Date, Description
        FROM Transactions
        WHERE User_ID=%s
        ORDER BY Transaction_Date DESC, Transaction_ID DESC
    """, (user_id,))

    rows = cur.fetchall()

    cur.close()
    con.close()

    return render_template("transactions.html", rows=rows)


# Delete Transaction
@app.route("/delete_transaction/<int:tid>", methods=["POST"])
def delete_transaction(tid):
    user_id = get_user_id()

    if not user_id:
        return redirect("/login")

    con = db_connect()
    cur = con.cursor()

    cur.execute(
        "DELETE FROM Transactions WHERE Transaction_ID=%s AND User_ID=%s",
        (tid, user_id)
    )

    con.commit()
    cur.close()
    con.close()

    return redirect("/transactions")


# Set or Update Monthly Budget
@app.route("/budget", methods=["GET", "POST"])
def budget():
    user_id = get_user_id()

    if not user_id:
        return redirect("/login")

    msg = ""

    if request.method == "POST":
        month = request.form["month"]
        year = request.form["year"]
        amount = request.form["amount"]

        if month == "" or year == "" or amount == "":
            msg = "Please fill in all fields."
        else:
            try:
                amount = float(amount)
                if amount <= 0:
                    msg = "Budget amount must be greater than zero."
                else:
                    con = db_connect()
                    cur = con.cursor()

                    cur.execute("""
                        INSERT INTO Budgets (User_ID, Budget_Month, Budget_Year, Amount)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (User_ID, Budget_Month, Budget_Year)
                        DO UPDATE SET Amount=EXCLUDED.Amount
                    """, (user_id, month, year, amount))

                    con.commit()
                    cur.close()
                    con.close()
                    msg = "Monthly budget saved successfully."
            except ValueError:
                msg = "Please enter a valid budget amount."

    con = db_connect()
    cur = con.cursor()

    cur.execute("""
        SELECT Budget_Month, Budget_Year, Amount
        FROM Budgets
        WHERE User_ID=%s
        ORDER BY Budget_Year DESC, Budget_Month DESC
    """, (user_id,))

    budgets = cur.fetchall()

    cur.close()
    con.close()

    return render_template("budget.html", budgets=budgets, msg=msg)


# Monthly Report
@app.route("/reports")
def reports():
    user_id = get_user_id()

    if not user_id:
        return redirect("/login")

    con = db_connect()
    cur = con.cursor()

    cur.execute("""
        SELECT
            TO_CHAR(DATE_TRUNC('month', Transaction_Date), 'Month YYYY'),
            SUM(CASE WHEN Transaction_Type='Income' THEN Amount ELSE 0 END),
            SUM(CASE WHEN Transaction_Type='Expense' THEN Amount ELSE 0 END)
        FROM Transactions
        WHERE User_ID=%s
        GROUP BY DATE_TRUNC('month', Transaction_Date)
        ORDER BY DATE_TRUNC('month', Transaction_Date) DESC
    """, (user_id,))

    report_data = cur.fetchall()

    cur.close()
    con.close()

    return render_template("reports.html", report_data=report_data)


# Logout
@app.route("/logout")
def logout():
    response = make_response(redirect("/"))
    response.delete_cookie("budget_user_id")
    return response


if __name__ == "__main__":
    create_table()
    app.run(debug=True)
