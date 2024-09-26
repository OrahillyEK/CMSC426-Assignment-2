from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

product_service_URL = 'http://127.0.0.1:5000/products'

#initialize cart contents dictionary
usercarts = {}


#retrieves products in the user's cart currently
@app.route('/cart/<user_id>', methods=['GET'])
def get_cart(user_id):     #to find the contents of the user's cart
    cart= usercarts.get(user_id, {})
    return jsonify(cart), 200


#adds product to the user's cart
@app.route('cart/<user_id>/add/<int:product_id>', methods=['POST'])
def add_product_to_cart(user_id, product_id):
    data = request.json


    #Checks for product in product service
    response = requests.get(f"{product_service_URL}/{product_id}")

    if response.status_code != 200:      #if product ID doesn't exist
        return jsonify({"error": "Product not found"}), 404
  
    product = response.json()

    #checks the stock exists
    if product['stock'] < 1:
        return jsonify({"error": "No stock available"}), 400
    
    #adds user's cart to usercarts
    if user_id not in usercarts:
        usercarts[user_id] = {}

    #adds the product to the user's cart
    if product_id in usercarts[user_id]:
        usercarts[user_id][product_id] += 1  #adds to existing quantity
    else: 
        usercarts[user_id][product_id] = 1   #adds new product quantity

    decrement_response = requests.post(f"{product_service_URL}/add_to_cart{product_id}")

    if decrement_response.status_code != 200:
        return jsonify({"message": "Failure to decrease stock"}), 500
    return jsonify({"message": "Product added to cart", "cart": usercarts[user_id]}), 201



if __name__ == "__main__":
    app.run(debug=True, port=5001)