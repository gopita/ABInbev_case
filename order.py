from models import Order

class OrderManager:
    def __init__(self, user, cart_items):
        self.order = Order(user, cart_items)

    def place_order(self):
        self.order.place_order()
        return "Order placed successfully"
