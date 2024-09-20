import sqlite3
from models import User
import hashlib


class Auth:
    def get_db_connection(self):
        # Create a new database connection for every request
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row  # Optional: to access rows as dictionaries
        return conn

    def register(self, username, password, name, email):
        conn = self.get_db_connection()
        c = conn.cursor()

        # Check if the username already exists
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = c.fetchone()

        if existing_user:
            conn.close()
            return "Username already exists"

        # Automatically assign "user" role during registration
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        c.execute("INSERT INTO users (username, password, role, name, email) VALUES (?, ?, ?, ?, ?)",
                  (username, hashed_password, 'user', name, email))
        conn.commit()
        conn.close()
        return "User registered successfully"

    def login(self, username, password):
        conn = self.get_db_connection()
        c = conn.cursor()

        # Use the User model's login method to verify the user
        if User.login(username, password):
            conn.close()
            return "Login successful"
        conn.close()
        return "Invalid username or password"

    def get_role(self, username):
        # Get the role of a user by username
        return User.get_role(username)
