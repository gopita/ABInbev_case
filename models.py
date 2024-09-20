import sqlite3
import hashlib

# User Model
class User:
    def __init__(self, username, password, role="user", name=None, email=None):
        self.username = username
        self.password = self.hash_password(password)
        self.role = role
        self.name = name
        self.email = email

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def save(self):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password, role, name, email) VALUES (?, ?, ?, ?, ?)",
                  (self.username, self.password, self.role, self.name, self.email))
        conn.commit()
        conn.close()

    @staticmethod
    def login(username, password):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT password FROM users WHERE username = ?", (username,))
        stored_password = c.fetchone()
        conn.close()

        if stored_password and User.hash_password(password) == stored_password[0]:
            return True
        return False

    @staticmethod
    def get_role(username):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT role FROM users WHERE username = ?", (username,))
        role = c.fetchone()
        conn.close()
        return role[0] if role else None


# Product Model
class Product:
    def __init__(self, name, price, stock, description):
        self.name = name
        self.price = price
        self.stock = stock
        self.description = description

    @staticmethod
    def get_all_products():
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT id, name, price, stock, description FROM products")
        products = c.fetchall()
        conn.close()
        return [{'id': row[0], 'name': row[1], 'price': row[2], 'stock': row[3], 'description': row[4]} for row in products]

    def save(self):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO products (name, price, stock, description) VALUES (?, ?, ?, ?)",
                  (self.name, self.price, self.stock, self.description))
        conn.commit()
        conn.close()


# Cart Model
class Cart:
    @staticmethod
    def get_cart(username):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''SELECT products.id, products.name, products.price, cart.quantity
                     FROM cart 
                     JOIN products ON cart.product_id = products.id
                     WHERE cart.username = ?''', (username,))
        items = c.fetchall()
        conn.close()
        return items

    @staticmethod
    def add_to_cart(username, product_id, quantity):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO cart (username, product_id, quantity) VALUES (?, ?, ?)",
                  (username, product_id, quantity))
        conn.commit()
        conn.close()

    @staticmethod
    def remove_from_cart(username, product_id):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("DELETE FROM cart WHERE username = ? AND product_id = ?", (username, product_id))
        conn.commit()
        conn.close()


# Order Model
class Order:
    @staticmethod
    def place_order(username, items):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        # Insert order into the orders table
        c.execute("INSERT INTO orders (username) VALUES (?)", (username,))
        order_id = c.lastrowid

        # Insert each product in the order
        for product_id, quantity in items:
            c.execute("INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)",
                      (order_id, product_id, quantity))

            # Update the product stock
            c.execute("UPDATE products SET stock = stock - ? WHERE id = ?", (quantity, product_id))

        conn.commit()
        conn.close()

    @staticmethod
    def clear_cart(username):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("DELETE FROM cart WHERE username = ?", (username,))
        conn.commit()
        conn.close()


# Create Tables
def create_tables():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Create users table with name and email columns
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'user',
                    name TEXT,
                    email TEXT
                )''')

    # Create products table with stock and description columns
    c.execute('''CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    price REAL NOT NULL,
                    stock INTEGER NOT NULL,
                    description TEXT
                )''')

    # Create the cart table with the quantity column
    c.execute('''CREATE TABLE IF NOT EXISTS cart (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    product_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    FOREIGN KEY (username) REFERENCES users(username),
                    FOREIGN KEY (product_id) REFERENCES products(id)
                )''')

    # Create the orders table
    c.execute('''CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (username) REFERENCES users(username)
                )''')

    # Create the order_items table to store products related to each order
    c.execute('''CREATE TABLE IF NOT EXISTS order_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    FOREIGN KEY (order_id) REFERENCES orders(id),
                    FOREIGN KEY (product_id) REFERENCES products(id)
                )''')

    conn.commit()
    conn.close()

# Call the function to create tables when the module is loaded
create_tables()
