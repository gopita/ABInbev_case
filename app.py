from flask import Flask, request, jsonify
import json
import hashlib
import os

app = Flask(__name__)

# Load or initialize data
def load_data():
    if not os.path.exists('data.json'):
        return {"users": [], "products": [], "orders": []}
    with open('data.json', 'r') as f:
        return json.load(f)

def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f)

data = load_data()

# Helper function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# User Registration
@app.route('/register', methods=['POST'])
def register():
    user_data = request.json
    user_data['password'] = hash_password(user_data['password'])
    data['users'].append(user_data)
    save_data(data)
    return jsonify({"message": "User registered successfully"})

# User Login
@app.route('/login', methods=['POST'])
def login():
    user_data = request.json
    hashed_password = hash_password(user_data['password'])
    for user in data['users']:
        if user['username'] == user_data['username'] and user['password'] == hashed_password:
            return jsonify({"message": "Login successful"})
    return jsonify({"error": "Invalid credentials"}), 401

# Add Product (Admin only)
@app.route('/products', methods=['POST'])
def add_product():
    product_data = request.json
    data['products'].append(product_data)
    save_data(data)
    return jsonify({"message": "Product added successfully"})

# View Products
@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(data['products'])

# Add to Cart
@app.route('/cart', methods=['POST'])
def add_to_cart():
    cart_item = request.json
    for user in data['users']:
        if user['username'] == cart_item['username']:
            if 'cart' not in user:
                user['cart'] = []
            user['cart'].append(cart_item['product'])
            save_data(data)
            return jsonify({"message": "Added to cart"})
    return jsonify({"error": "User not found"}), 404

# Place Order
@app.route('/order', methods=['POST'])
def place_order():
    order_data = request.json
    for user in data['users']:
        if user['username'] == order_data['username']:
            if 'cart' not in user or not user['cart']:
                return jsonify({"error": "Cart is empty"}), 400
            order = {"username": order_data['username'], "order": user['cart']}
            data['orders'].append(order)
            user['cart'] = []
            save_data(data)
            return jsonify({"message": "Order placed successfully"})
    return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
