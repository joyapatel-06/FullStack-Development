from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def employee():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        dept = request.form['dept']

        return f'''
        Name: {name}<br>
        Age: {age}<br>
        Department: {dept}
        '''

    return '''
    <form method="post">
        Name: <input type="text" name="name"><br>
        Age: <input type="text" name="age"><br>
        Department: <input type="text" name="dept"><br>
        <input type="submit" value="Submit">
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)