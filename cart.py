from models import Product, c  # Import the cursor from models.py

class CartManager:
    def __init__(self, user):
        self.user = user
        self.items = []

    def add_to_cart(self, product_name, quantity):
        product = self.get_product_by_name(product_name)
        if product and product.stock >= quantity:
            self.items.append((product, quantity))
            product.stock -= quantity
            product.save()
            return f"{quantity} of {product_name} added to cart"
        return "Product not found or not enough stock"

    def get_product_by_name(self, product_name):
        c.execute("SELECT * FROM products WHERE name = ?", (product_name,))
        row = c.fetchone()
        if row:
            return Product(row[1], row[2], row[3])  # row[1] is name, row[2] is price, row[3] is stock
        return None

    def view_cart(self):
        return self.items

    def clear_cart(self):
        self.items = []
