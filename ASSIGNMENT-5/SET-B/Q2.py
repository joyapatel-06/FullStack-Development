from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form['name']
        rating = request.form['rating']
        comments = request.form['comments']

        return f'''
        Name: {name}<br>
        Rating: {rating}<br>
        Comments: {comments}
        '''

    return '''
    <form method="post">
        Name: <input type="text" name="name"><br>
        Rating: <input type="text" name="rating"><br>
        Comments: <textarea name="comments"></textarea><br>
        <input type="submit">
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)