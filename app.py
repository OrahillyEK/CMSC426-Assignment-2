from flask import Flask, jsonify, request

app= Flask(__name__)

#Filler products available
products = [
    {"id": 1, "title": "Eggs", "price": 2.00, "on_hand": 4},
    {"id": 2, "title": "Bread", "price": 1.50, "on_hand": 17},
    {"id": 3, "title": "Milk", "price": 3.00, "on_hand": 11},
    {"id": 4, "title": "Apple", "price": 0.50, "on_hand": 24},
]

#endpoint 1 retrieves a list of all products with names, prices, and stock.
@app.route('/products', methods=['GET'])
def get_product_info():
    return jsonify({"products": products})

#endpoint 2 retrieves information about a specific product based on it's productid
@app.route('/products/<int:product_id>', methods=['GET'])
def get_single_product(product_id):
    product = next((product for product in products if product["id"] == product_id), None)
    if product:
        return jsonify ({"product": product})
    else: return jsonify ({"error": "Task not found"}), 404

    