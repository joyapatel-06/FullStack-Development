from flask import Flask, request, jsonify

app = Flask(__name__)

students = []

# GET API
@app.route('/student', methods=['GET'])
def get_student():
    return jsonify(students)

# POST API
@app.route('/addstudent', methods=['POST'])
def add_student():
    data = request.get_json()

    students.append(data)

    return jsonify({
        "message": "Student added successfully",
        "student": data
    })

if __name__ == '__main__':
    app.run(debug=True)