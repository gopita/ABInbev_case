import unittest
from auth import Auth
from product import ProductManager
from cart import CartManager

class TestEcommerceBackend(unittest.TestCase):
    def test_user_registration(self):
        auth = Auth()
        result = auth.register("alice", "alice123")
        self.assertEqual(result, "User registered successfully")

    def test_add_product(self):
        result = ProductManager.add_product("Keyboard", 100, 5)
        self.assertEqual(result, "Product added successfully")

if __name__ == '__main__':
    unittest.main()
