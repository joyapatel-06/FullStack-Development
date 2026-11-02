from flask import Flask, request

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def home():

    if request.method =="POST":
        name = request.form.get("name")

        return f"""
        <h2>Hello!{name}</h2>
"""
    return"""
<h2>Student Info</h2>
<form method="POST">
Name:
<input type="text"  name="name">
<br><br>

<input type="submit" value="submit">
</form>
"""

if __name__ == "__main__":
    app.run(debug=True)