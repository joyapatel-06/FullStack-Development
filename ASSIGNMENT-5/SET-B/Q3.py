from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def salary():
    if request.method == 'POST':
        basic = float(request.form['basic'])
        allowance = 5000
        total = basic + allowance

        return f"Total Salary = {total}"

    return '''
    <form method="post">
        Basic Salary:
        <input type="text" name="basic"><br>
        <input type="submit" value="Calculate">
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)