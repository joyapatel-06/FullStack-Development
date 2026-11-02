from flask import Flask ,request

app = Flask(__name__)

@app.route('/student', methods=['GET'])
def student():
    return "Student Details..! Recieved using Get Request."
if __name__=='__main__':
    app.run(debug=True)