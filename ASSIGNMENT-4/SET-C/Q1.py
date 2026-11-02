from flask import Flask

app = Flask(__name__)

@app.route('/product/<int:pid>')
def product(pid):
    return f"""
    <h1>Product Details</h1>
    <p>Product ID: {pid}</p>
    <p>Product Name: Laptop</p>
    <p>Price: ₹50,000</p>
    """

if __name__ == '__main__':
    app.run(debug=True)