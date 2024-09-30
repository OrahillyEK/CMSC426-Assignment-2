from flask import Flask, jsonify, request
import requests, os

app = Flask(__name__)

product_service_URL = 'http://127.0.0.1:5000/products'

@app.route('/')
def oops():
    return "Hey! You made it!"

#initialize cart contents dictionary
usercarts = {}


#retrieves products in the user's cart currently
@app.route('/cart/<user_id>', methods=['GET'])
def get_cart(user_id):     #to find the contents of the user's cart
    cart= usercarts.get(user_id, {})
    return jsonify(cart), 200


#adds product to the user's cart
@app.route('/cart/<user_id>/add/<int:product_id>', methods=['POST'])
def add_product_to_cart(user_id, product_id):
    data = request.get_json()
    quantity = data.get('quantity')


    #Checks for product in product service
    response = requests.get(f"{product_service_URL}/{product_id}")

    if response.status_code != 200:      #if product ID doesn't exist
        return jsonify({"error": "Product not found"}), 404
  
    product = response.json()

    product_data = product.get('product') #to access the stock in the nested library
    if not product_data:
        return jsonify({"error": "No stock available"}), 400

    #adds user's cart to usercarts
    if user_id not in usercarts:
        usercarts[user_id] = {}

    #adds the product to the user's cart
    if product_id in usercarts[user_id]:
        usercarts[user_id][product_id] += quantity  #adds to existing quantity
    else: 
        usercarts[user_id][product_id] = quantity   #adds new product quantity

    decrement_response = requests.post(f"{product_service_URL}/add_to_cart/{product_id}", json = {"quantity" : quantity})

    if decrement_response.status_code != 200: #in case the decrement doesn't work
        return jsonify({"message": "Failure to decrease stock"}), 500
    

    return jsonify({"message": "Product added to cart", "cart": usercarts[user_id]}), 201


#removes an item from the user's cart and adds it back to the stock of the product service
@app.route('/cart/<user_id>/remove/<int:product_id>', methods=['POST'])
def remove_product_from_cart(user_id, product_id):
    # Check if the user has a cart
    if user_id not in usercarts or product_id not in usercarts[user_id]:
        return jsonify({"error": "Product not found in cart"}), 404

    # Get the quantity of the product being removed
    data = request.get_json()
    remove_quantity = data.get('quantity')

    current_quantity = usercarts[user_id][product_id]

    if remove_quantity > current_quantity:
        return jsonify({"error": "Not enough in cart"}), 400
    
    # Remove the product from the user's cart
    usercarts[user_id][product_id] -= remove_quantity

    # Add the stock back to the product
    decrement_response = requests.post(f"{product_service_URL}/add_stock/{product_id}", json={"quantity": remove_quantity})

    if decrement_response.status_code != 200:  # If stock addition fails
        return jsonify({"message": "Failure to increase stock"}), 500

    return jsonify({"message": "Product removed from cart", "cart": usercarts[user_id]}), 200



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port)
