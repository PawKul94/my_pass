from create_pass import create_password
from os import path
from tkinter import messagebox
from tkinter import *
from tkinter.ttk import *
import json
import pyperclip
import re

FONT = ("Courier", 10, "bold")


class MyPass(Tk):
    def __init__(self):
        super().__init__()
        self.title("My Pass")
        self.config(padx=20, pady=20)
        self.resizable(width=False, height=False)
        # Create image
        self.image = PhotoImage(file="logo.png")
        self.canvas = Canvas(width=200, height=200)
        self.canvas.create_image(100, 100, image=self.image)
        self.canvas.grid(row=0, column=1)
        # Website label + entry
        self.website_label = Label(text="Website:", font=FONT)
        self.website_label.grid(row=1, column=0, padx=2, pady=2, sticky="W")
        self.website_entry = Entry(width=35)
        self.website_entry.focus_set()
        self.website_entry.grid(row=1, column=1, padx=2, pady=2, sticky="W")
        # Username label + entry
        self.username_label = Label(text="E-mail / Username:", font=FONT)
        self.username_label.grid(row=2, column=0, padx=2, pady=2, sticky="W")
        self.username_entry = Entry(width=56)
        self.username_entry.insert(0, "frogus12@gmail.com")
        self.username_entry.grid(row=2, column=1, columnspan=2, padx=2, pady=2, sticky="W")
        # Password label + entry
        self.password_label = Label(text="Password:", font=FONT)
        self.password_label.grid(row=3, column=0, padx=2, pady=2, sticky="W")
        self.password_entry = Entry(width=35)
        self.password_entry.grid(row=3, column=1, padx=2, pady=2, sticky="W")
        # Search button
        self.search_button = Button(text="Search", width=18, command=self.retrieve_credentials)
        self.search_button.grid(row=1, column=2, padx=2, pady=2)
        # Generate password button
        self.password_generate_button = Button(text="Generate Password", width=18, command=self.generate_password)
        self.password_generate_button.grid(row=3, column=2, padx=2, pady=2)
        # Add button
        self.add_button = Button(text="Add", width=56, command=self.save_credentials)
        self.add_button.grid(row=4, column=1, columnspan=2, padx=2, pady=2, sticky="W")

        self.mainloop()

    def check_for_duplicate(self):
        site = self.website_entry.get().capitalize()

        if path.exists("data.json"):
            try:
                with open("data.json", "r") as f:
                    data = json.load(f)
                    if site in data:
                        return False
            except json.decoder.JSONDecodeError:
                return True
        return True

    def generate_password(self):
        self.password_entry.delete(0, "end")
        password = create_password()
        pyperclip.copy(password)
        self.password_entry.insert(0, password)

    def retrieve_credentials(self):
        website = self.website_entry.get().capitalize()

        if website == "":
            messagebox.showerror("Website error", "Please provide a website!")
        elif path.exists("data.json"):
            try:
                with open("data.json", "r") as f:
                    data = json.load(f)
            except json.decoder.JSONDecodeError:
                data = {}

            if website in data.keys():
                if messagebox.askquestion("Credentials",
                                          f"{website}\nUsername: {data[website]['username']}\n"
                                          f"Password: {data[website]['password']}\n"
                                          "Do you want to copy the password?") == "yes":
                    pyperclip.copy(data[website]['password'])
            else:
                messagebox.showinfo("Credentials", f"No entry for {website}.")

    def save_credentials(self):
        website = self.website_entry.get().capitalize()
        username = self.username_entry.get()
        password = self.password_entry.get()
        new_data = {website: {"username": username, "password": password}}

        if self.validate_inputs():
            if not path.exists("data.json"):
                with open("data.json", "w") as f:
                    json.dump(new_data, f, indent=4)
            else:
                try:
                    with open("data.json", "r") as f:
                        data = json.load(f)
                        data.update(new_data)
                except json.decoder.JSONDecodeError:
                    data = new_data

                with open("data.json", "w") as f:
                    json.dump(data, f, indent=4)

            self.website_entry.delete(0, "end")
            self.username_entry.delete(0, "end")
            self.password_entry.delete(0, "end")

    def validate_inputs(self):
        if self.website_entry.get() == '':
            messagebox.showerror("Website error", "Please provide a website!")
            return False
        elif self.username_entry.get() == '':
            messagebox.showerror("Username error", "Please provide an username!")
            return False
        elif self.password_entry.get() == '':
            messagebox.showerror("Password error", "Please provide a password!")
            return False
        elif not self.check_for_duplicate():
            website = self.website_entry.get().capitalize()
            if not messagebox.askyesno("Duplicate error", f"You already have a password stored for {website}. "
                                                          "Do you want to overwrite it?"):
                return False
        elif not self.validate_password():
            if not messagebox.askyesno("Weak password", "Your password appears weak. Do you want to proceed?"):
                return False
        return True

    def validate_password(self):
        password = self.password_entry.get()

        uppercase = True if re.search("[A-Z]", password) else False
        lowercase = True if re.search("[a-z]", password) else False
        digit = True if re.search("[0-9]", password) else False
        symbol = True if re.search("\W", password) else False
        length = True if len(password) in range(8, 33) else False
        contains_word_password = True if re.search("password", password.lower()) else False

        if all([uppercase, lowercase, digit, symbol, length]) and not contains_word_password:
            return True
        else:
            return False


if __name__ == "__main__":
    app = MyPass()
