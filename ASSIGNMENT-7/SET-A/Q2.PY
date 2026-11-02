from flask import Flask, request, jsonify

app = Flask(__name__)

employee = []

@app.route('/employee', methods=['GET'])
def get_employee():
    return jsonify(employee)

@app.route('/addemployee', methods=['POST'])
def add_employee():
    data = request.get_json()
    employee.append(data)

    return jsonify({
        "msg": "Employee added successfully",
        "employee": data
    })

if __name__ == '__main__':
    app.run(debug=True)