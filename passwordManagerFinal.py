import tkinter as tk
from tkinter import simpledialog, messagebox
from cryptography.fernet import Fernet
import json
import pyperclip
import base64

# gen or load encryption key
def generate_key():
    return Fernet.generate_key()

def load_key():
    try:
        with open("key.key", "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        key = generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)
        return key

# create instance of fernet class using key
key = load_key()
fernet = Fernet(key)

# load exsisting passwords or create
def load_passwords_from_file():
    try:
        with open("passwords.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# create dictionary to load passwords and save them
passwords = load_passwords_from_file()

# Function to save passwords to the file
def save_passwords_to_file():
    with open("passwords.json", "w") as file:
        serializable_passwords = {account: base64.b64encode(encrypted_password).decode() for account, encrypted_password in passwords.items()}
        json.dump(serializable_passwords, file)

# generate password and copy it to clipboard
def generate_password():
    password_length = simpledialog.askinteger("Generate Password", "Enter the length of the password:")
    if password_length:
        password = generate_random_password(password_length)
        pyperclip.copy(password)  # Copy the password to the clipboard
        messagebox.showinfo("Generated Password", "Password has been generated and copied to the clipboard.")

# save password
def save_password():
    account = simpledialog.askstring("Save Password", "Enter Account Name:")
    if account:
        password = simpledialog.askstring("Save Password", "Enter Password:")
        if password:
            encrypted_password = fernet.encrypt(password.encode())
            passwords[account] = encrypted_password
            save_passwords_to_file()
            messagebox.showinfo("Success", "Password saved successfully!")

# retrieve password
def retrieve_password():
    account = simpledialog.askstring("Retrieve Password", "Enter Account Name:")
    if account:
        if account in passwords:
            serialized_password = passwords[account]
            encrypted_password = base64.b64decode(serialized_password.encode())
            decrypted_password = fernet.decrypt(encrypted_password).decode()
            pyperclip.copy(decrypted_password)  # Copy the decrypted password to the clipboard
            messagebox.showinfo("Password", f"Password for {account}: {decrypted_password} (copied to clipboard)")
        else:
            messagebox.showwarning("Error", "Account not found.")

# generate strong password 
import string
import random

def generate_random_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

# create a Tkinter window
window = tk.Tk()
window.title("Password Manager")

# create GUI buttons
generate_button = tk.Button(window, text="Generate Password", command=generate_password)
save_button = tk.Button(window, text="Save Password", command=save_password)
retrieve_button = tk.Button(window, text="Retrieve Password", command=retrieve_password)

# pack buttons
generate_button.pack()
save_button.pack()
retrieve_button.pack()

window.mainloop()
