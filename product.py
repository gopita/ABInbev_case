from models import Product

class ProductManager:
    @staticmethod
    def add_product(name, price, stock):
        product = Product(name, price, stock)
        product.save()
        return "Product added successfully"
