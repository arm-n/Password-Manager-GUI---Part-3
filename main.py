from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# --------------------------------- PASSWORD GENERATOR -----------------------#
def generate_password():
    """Generates a random password and inserts it into the password field"""
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numbers = "0123456789"
    symbols = "!#$%&()*+"

    password_letters = [random.choice(letters) for _ in range(5)]
    password_symbols = [random.choice(symbols) for _ in range(5)]
    password_numbers = [random.choice(numbers) for _ in range(5)]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    password = "".join(password_list)
    password_input.delete(0, END)  # Clear previous password
    password_input.insert(0, password)
    pyperclip.copy(password)  # Copy to clipboard

# ---------------------------------- SAVE PASSWORD -----------------------#
def save():
    """Saves the website, username, and password in a JSON file"""
    website = website_input.get().strip()
    username = username_input.get().strip()
    password = password_input.get().strip()
    new_data = {website: {"Username": username, "Password": password}}

    if not website or not username or not password:
        messagebox.showerror(title="Error", message="Please enter all details.")
        return

    try:
        with open("data.json", "r") as file:
            data = json.load(file)  # Load existing data
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}  # Create a new file if not found or corrupted

    data.update(new_data)  # Update data dictionary

    try:
        with open("data.json", "w") as file:
            json.dump(data, file, indent=4)  # Save updated data
    except Exception as e:
        messagebox.showerror(title="Error", message=f"Could not save data: {e}")
        return

    website_input.delete(0, END)
    password_input.delete(0, END)

#------------------------- SEARCH --------------------------------------#
def search_website():
    """Searches for saved login details for a given website"""
    website = website_input.get().strip()

    if not website:
        messagebox.showwarning(title="Warning", message="Enter a website name.")
        return

    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showerror(title="Error", message="No saved data available.")
        return

    if website in data:
        username = data[website]['Username']
        password = data[website]["Password"]
        messagebox.showinfo(title=website, message=f"Username: {username}\nPassword: {password}")
    else:
        messagebox.showerror(title="Error", message="No details found.")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Logo
try:
    logo = PhotoImage(file="logo.png")
    canvas = Canvas(width=200, height=200)
    canvas.create_image(100, 100, image=logo)
    canvas.grid(row=0, column=1)
except:
    messagebox.showwarning("Warning", "Logo image not found. Proceeding without logo.")

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0, sticky="w")

username_label = Label(text="Email/Username:")
username_label.grid(row=2, column=0, sticky="w")

password_label = Label(text="Password:")
password_label.grid(row=3, column=0, sticky="w")

# Entry Fields
website_input = Entry(width=35)
website_input.grid(row=1, column=1, sticky="w")
website_input.focus()

username_input = Entry(width=35)
username_input.grid(row=2, column=1, columnspan=2, sticky="w")
username_input.insert(0, "mohammedarmaand@gmail.com")  # Default email

password_input = Entry(width=35)
password_input.grid(row=3, column=1, sticky="w")

# Buttons
password_button = Button(text="Generate Password", command=generate_password)
password_button.grid(row=3, column=2, sticky="w")

search_button = Button(text="Search", width=14, command=search_website)
search_button.grid(row=1, column=2)

add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
