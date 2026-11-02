from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def feedback():

    if request.method == 'POST':
        name = request.form['name']
        feedback = request.form['feedback']

        return f'''
        <h2>Thank You, {name}!</h2>
        <p>Your Feedback: {feedback}</p>
        '''

    return '''
    <h2>Feedback Form</h2>

    <form method="POST">
        Name:
        <input type="text" name="name" required>
        <br><br>

        Feedback:
        <textarea name="feedback" required></textarea>
        <br><br>

        <input type="submit" value="Submit Feedback">
    </form>
    '''
if __name__ == '__main__':
    app.run(debug=True)