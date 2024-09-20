import tkinter as tk
import requests
import json

BASE_URL = 'http://127.0.0.1:5000'

# Function to register a new user
def register():
    username = entry_username.get()
    password = entry_password.get()
    response = requests.post(f'{BASE_URL}/register', json={"username": username, "password": password})
    label_status.config(text=response.json().get('message'))

# Function to log in
def login():
    username = entry_username.get()
    password = entry_password.get()
    response = requests.post(f'{BASE_URL}/login', json={"username": username, "password": password})
    label_status.config(text=response.json().get('message'))

# Main Window
window = tk.Tk()
window.title('E-Commerce')

tk.Label(window, text="Username:").pack()
entry_username = tk.Entry(window)
entry_username.pack()

tk.Label(window, text="Password:").pack()
entry_password = tk.Entry(window, show="*")
entry_password.pack()

btn_register = tk.Button(window, text="Register", command=register)
btn_register.pack()

btn_login = tk.Button(window, text="Login", command=login)
btn_login.pack()

label_status = tk.Label(window, text="")
label_status.pack()

window.mainloop()
