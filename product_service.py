from flask import Flask, jsonify, request

app= Flask(__name__)

#Filler products available
products = {
    1: {"id": 1, "title": "Eggs", "price": 2.00, "stock": 4},
    2: {"id": 2, "title": "Bread", "price": 1.50, "stock": 17},
    3: {"id": 3, "title": "Milk", "price": 3.00, "stock": 11},
    4: {"id": 4, "title": "Apple", "price": 0.50, "stock": 24},
}

#this endpoint is just here to give render something to jump to
@app.route('/', methods=['GET'])
def oops():
    return jsonify({"message": "Well, here you are!"}), 200

#endpoint 1 retrieves a list of all products with names, prices, and stock.
@app.route('/products', methods=['GET'])
def get_product_info():
    return jsonify({"products": products})

#endpoint 2 retrieves information about a specific product based on it's productid
@app.route('/products/<int:product_id>', methods=['GET'])
def get_single_product(product_id):
    product = products.get(product_id)
    if product:
        return jsonify ({"product": product})
    else: return jsonify ({"error": "Product not found"}), 404

#endpoint 3 allows for adding new grocery products to the list with an id, title, price, and "on_hand" quantity
@app.route('/products', methods =['POST'])
def add_new_product():
    data = request.json
    product_id = max(products.keys()) +1     #Set the ID to next avail
    products[product_id] = {
        "name": data['name'],
        "price": data['price'],
        "stock": data['stock']
    }
    return jsonify({"message": "Your product has been created"}), 201

#endpoint to decrease stock of product when added to cart
@app.route('/products/add_to_cart<int:product_id>', methods =['POST'])
def decrement_stock(product_id):
    product_in_cart= products.get(product_id)
    if not product_in_cart:     #if the id doesn't exist
        return jsonify ({"error": "Product not found"}), 404 
    
    data = request.get_json()
    quantity = data.get('quantity', 1) #decrement by 1 if no quantity passed
    
    if product_in_cart['stock'] <= quantity:     #if the stock is zero, out of stock
        return jsonify({"error": "Product out of stock"}), 400  
    
    product_in_cart['stock'] -= quantity     #Reduce stock by one unit
    return jsonify({"message": "Product stock decremented"}), 200 
    


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Fallback to 5000 if PORT is not set
    app.run(host='0.0.0.0', port=port)

