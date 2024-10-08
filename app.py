from auth import Auth
from models import User, Product, Cart, Order
from flask import Flask, render_template, request, redirect, url_for, session, flash
import hashlib

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necessary for session handling

auth = Auth()

# Home route redirects to register
@app.route('/')
def home():
    return redirect(url_for('login'))

# Route for Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        email = request.form['email']

        # Call the Auth class to register the user
        message = auth.register(username, password, name, email)
        return render_template('success.html', message=message)
    
    return render_template('register.html')

# Route for Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        message = auth.login(username, password)
        if message == "Login successful":
            session['username'] = username  # Store the username in session
            return redirect(url_for('products'))  # Redirect to the products page
        return render_template('success.html', message=message)
    return render_template('login.html')


# Route for Profile
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if not authenticated
    
    username = session['username']

    # Retrieve user data from the database
    conn = auth.get_db_connection()
    c = conn.cursor()
    c.execute("SELECT username, name, email FROM users WHERE username = ?", (username,))
    user = c.fetchone()

    if request.method == 'POST':
        # Get the new data from the form
        new_name = request.form['name']
        new_email = request.form['email']
        new_password = request.form['password']

        # Hash the new password if provided, else keep the old one
        hashed_password = hashlib.sha256(new_password.encode()).hexdigest() if new_password else None
        if hashed_password:
            c.execute("UPDATE users SET name = ?, email = ?, password = ? WHERE username = ?",
                      (new_name, new_email, hashed_password, username))
        else:
            c.execute("UPDATE users SET name = ?, email = ? WHERE username = ?", (new_name, new_email, username))
        
        conn.commit()
        conn.close()

        # Show a success message
        flash('Profile updated successfully!', 'success')
        
        return redirect(url_for('profile'))  # Redirect back to profile after update

    return render_template('profile.html', user=user)

# Route for the Products Page
@app.route('/products')
def products():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    username = session['username']

    # Fetch user info (including name and role) from the database
    conn = auth.get_db_connection()
    c = conn.cursor()
    c.execute("SELECT name, role FROM users WHERE username = ?", (username,))
    user = c.fetchone()

    # Fetch products from the database
    all_products = Product.get_all_products()

    # Pass the user's name and role to the template
    return render_template('products.html', products=all_products, name=user['name'], role=user['role'])

# Add Product Route (admin only)
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    # Fetch the user's role
    role = User.get_role(username)

    if role != 'admin':
        flash('Only admins can add products.', 'danger')
        return redirect(url_for('products'))

    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        stock = int(request.form['stock'])
        description = request.form['description']

        # Save the new product
        product = Product(name=name, price=price, stock=stock, description=description)
        product.save()

        flash('Product added successfully!', 'success')
        return redirect(url_for('products'))

    return render_template('add_product.html')


# Edit Product Route (admin only)
@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    
    # Fetch the user's role
    role = User.get_role(username)

    if role != 'admin':
        flash('Only admins can edit products.', 'danger')
        return redirect(url_for('products'))

    # Fetch product by id
    product = Product.get_by_id(product_id)

    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        stock = int(request.form['stock'])
        description = request.form['description']

        # Ensure that the product ID is passed to the update method
        updated_product = Product(id=product_id)
        updated_product.update(product_id, name, price, stock, description)

        flash('Product updated successfully!', 'success')
        return redirect(url_for('products'))

    return render_template('edit_product.html', product=product)


# Remove Product Route (admin only)
@app.route('/remove_product/<int:product_id>', methods=['POST'])
def remove_product(product_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    # Fetch the user's role
    role = User.get_role(username)

    if role != 'admin':
        flash('Only admins can remove products.', 'danger')
        return redirect(url_for('products'))

    # Remove the product
    Product.remove(product_id)

    flash('Product removed successfully!', 'success')
    return redirect(url_for('products'))


# Cart Route
@app.route('/cart')
def cart():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    # Fetch the user's role from the database
    role = User.get_role(username)

    # Check if the user is an admin, deny access to the cart page if true
    if role == 'admin':
        flash('Admins do not have access to the cart page.', 'danger')
        return redirect(url_for('products'))  # Redirect them to the products page or another page

    # Fetch the cart items for the regular user
    cart_items = Cart.get_cart(username)

    return render_template('cart.html', cart_items=cart_items)

# Add to Cart Route
@app.route('/add_to_cart/<int:product_id>', methods=['GET', 'POST'])
def add_to_cart(product_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    # Fetch the user's role from the database
    role = User.get_role(username)

    # If the user is an admin, deny access to add items to the cart
    if role == 'admin':
        flash('Admins cannot add products to the cart.', 'danger')
        return redirect(url_for('products'))  # Redirect them to the products page

    # For non-admin users, add the product to the cart
    Cart.add_to_cart(username, product_id, 1)

    flash('Product added to cart!', 'success')
    return redirect(url_for('products'))


# Place Order Route
@app.route('/place_order', methods=['POST'])
def place_order():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    # Fetch the user's role from the database
    role = User.get_role(username)

    # If the user is an admin, deny access to place orders
    if role == 'admin':
        flash('Admins cannot place orders.', 'danger')
        return redirect(url_for('products'))  # Redirect to the products page

    # Fetch cart items and place the order for non-admin users
    cart_items = Cart.get_cart(username)

    if cart_items:
        # Extract items (product_id, quantity) from the cart
        items = [(item[0], item[3]) for item in cart_items]  # (product_id, quantity)

        # Place the order
        Order.place_order(username, items)

        # Clear the cart
        Order.clear_cart(username)

        flash('Order placed successfully!', 'success')

    return redirect(url_for('cart'))




@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    # Remove the item from the cart
    Cart.remove_from_cart(username, product_id)

    flash('Product removed from cart!', 'success')
    return redirect(url_for('cart'))


@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove the username from the session
    return redirect(url_for('login'))  # Redirect to the login page after logging out


if __name__ == '__main__':
    app.run(debug=True)
