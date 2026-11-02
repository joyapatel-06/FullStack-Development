from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        pname = request.form['pname']
        qty = int(request.form['qty'])
        price = float(request.form['price'])

        total = qty * price

        return f'''
        Product Name: {pname}<br>
        Quantity: {qty}<br>
        Price: {price}<br>
        Total Amount: {total}
        '''

    return '''
    <form method="post">
        Product Name:
        <input type="text" name="pname"><br>
        Quantity:
        <input type="number" name="qty"><br>
        Price:
        <input type="number" name="price"><br>
        <input type="submit" value="Order">
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)