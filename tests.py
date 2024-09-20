import unittest
from app import app
import sqlite3

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # Ensure the app context is pushed for each test
        with app.app_context():
            self.conn = sqlite3.connect('database.db')
            self.c = self.conn.cursor()

            self.conn.commit()


    # Test User Registration
    def test_user_registration(self):
        # Simulate user registration via the register route
        response = self.app.post('/register', data=dict(
            username='testuser',
            password='testpassword',
            name='Test User',
            email='testuser@example.com'
        ), follow_redirects=True)

        # Ensure that the response status code is 200 after redirection
        self.assertEqual(response.status_code, 200)

        # Query the database to ensure the user was registered
        self.c.execute("SELECT * FROM users WHERE username = ?", ('testuser',))
        user = self.c.fetchone()

        # Check if the user exists in the database
        self.assertIsNotNone(user)
        self.assertEqual(user[1], 'testuser')

    # Test Product Addition by Admin
    def test_add_product(self):
        # Simulate admin login
        with self.app:
            login_response = self.app.post('/login', data=dict(
                username='admin',
                password='admin'
            ), follow_redirects=True)

            # Ensure that login was successful
            self.assertEqual(login_response.status_code, 200)

            # Simulate adding a product by the admin
            response = self.app.post('/add_product', data=dict(
                name='Test Product',
                price=100.00,
                stock=50,
                description='This is a test product'
            ), follow_redirects=True)

            # Ensure that the response status code is 200 after redirection
            self.assertEqual(response.status_code, 200)

            # Query the database to ensure the product was added
            self.conn.commit()
            self.c.execute("SELECT * FROM products WHERE name = ?", ('Test Product',))
            product = self.c.fetchone()

            # Check if the product exists in the database
            self.assertIsNotNone(product)
            self.assertEqual(product[1], 'Test Product')

    # Test Order Placement
    def test_add_cart(self):
        # Simulate user login
        with self.app:
            login_response = self.app.post('/login', data=dict(
                username='testuser',
                password='testpassword'
            ), follow_redirects=True)

            # Ensure that login was successful
            self.assertEqual(login_response.status_code, 200)

            # Simulate adding the product to the cart
            response = self.app.post('/add_to_cart/1', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            # Query the database to ensure the product was added to cart
            self.conn.commit()
            self.c.execute("SELECT * FROM cart WHERE username = ?", ('testuser',))
            cart = self.c.fetchone()

            # Check if the produt exists in the table cart in the database
            self.assertIsNotNone(cart)
            self.assertEqual(cart[1], 'testuser')


if __name__ == '__main__':
    unittest.main()
