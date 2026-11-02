from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def rectangle():
    if request.method == 'POST':
        l = float(request.form['length'])
        b = float(request.form['breadth'])
        area = l * b
        return f"Area = {area}"

    return '''
    <form method="post">
        Length: <input type="text" name="length"><br>
        Breadth: <input type="text" name="breadth"><br>
        <input type="submit" value="Calculate">
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)