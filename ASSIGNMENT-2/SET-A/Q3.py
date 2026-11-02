from flask import Flask,request

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home():

    if request.method == "POST":
        num1 = int(request.form['num1'])
        num2 = int(request.form['num2'])
        return f"Product of{num1} and {num2} is {num1*num2}"

    return f'''
<h2>Product od Two Numbers</h2>
<form method="POST">
    Enter a First Number : <input type="number" name="num1">
    <br><br>

    Enter a Second Number : <input type="number" name="num2">
    <br><br>

    <input type="submit" value="product">
    </form>
    '''

if __name__ =='__main__':
    app.run(debug=True)