from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        marks = int(request.form['marks'])
        if marks >= 35:
            return "Pass"
        else:
            return "Fail"

    return '''
    <form method="post">
        Marks: <input type="text" name="marks">
        <input type="submit" value="Check">
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)