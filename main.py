from tkinter import *
from tkinter import messagebox  # Import messagebox module for displaying alerts
import random  # Import random module for generating random passwords
import pyperclip  # Import pyperclip module for copying passwords to clipboard
import json

# Define color constants for the UI
BLACK = "#222831"
GRAY = "#31363F"
CYAN = "#76ABAE"
WHITE = "#EEEEEE"

# Define character sets for generating passwords
lower_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
                 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
upper_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                 'U',
                 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_pass():
    # Clear any existing password in the entry field
    pass_in.delete(0, END)

    # Define random lengths for different character sets
    lr_letters = random.randint(5, 7)
    up_letters = random.randint(3, 5)
    nr_numbers = random.randint(2, 6)
    nr_symbols = random.randint(1, 4)

    # Generate random characters from each character set
    code1 = [random.choice(lower_letters) for _ in range(0, up_letters)]
    code2 = [random.choice(upper_letters) for _ in range(0, lr_letters)]
    code3 = [random.choice(symbols) for _ in range(0, nr_symbols)]
    code4 = [random.choice(numbers) for _ in range(0, nr_numbers)]

    # Concatenate and shuffle the characters to create a password
    list_code = code1 + code2 + code3 + code4
    random.shuffle(list_code)
    random.shuffle(list_code)
    random.shuffle(list_code)
    shuffled_passcode = "".join(list_code)

    # Insert the generated password into the entry field
    pass_in.insert(END, shuffled_passcode)

    # Copy the generated password to the clipboard
    pyperclip.copy(shuffled_passcode)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def fetch_seq():
    # Get user input for website, email, and password
    web = web_in.get().title()
    email = email_in.get()
    passw = pass_in.get()
    new_data = {
        web: {
            "email": email,
            "password": passw,
        }
    }

    # Check if website field are not empty
    if len(web) > 0:
        # Check if password meets the minimum length requirement
        if len(passw) > 8:
            # Ask for user confirmation before saving
            is_ok = messagebox.askokcancel(title=web, message=f"The information entered are:\n"
                                                              f"Email: {email}\n"
                                                              f"Password: {passw}\n"
                                                              f"Is it correct")

            if is_ok:
                # Format the information and save it to a json file
                try:
                    with open("passwords.json", "r") as file:
                        data = json.load(file)
                        data.update(new_data)

                except FileNotFoundError:
                    with open("passwords.json", "w") as file:
                        json.dump(new_data, file, indent=4)
                else:
                    with open("passwords.json", "w") as file:
                        json.dump(data, file, indent=4)

                # Show success message and clear input fields
                messagebox.showinfo(title=web, message="Save successful")
                web_in.delete(0, END)
                pass_in.delete(0, END)
        else:
            # Show warning message for weak password
            messagebox.showwarning(title="Weak Password",
                                   message=f"inputted password needs a minimum of 8 characters\n "
                                           f"current length: {len(passw)}")
    else:
        # Show warning message for empty fields
        messagebox.showwarning(title="Oops", message="Please don't leave any field empty!")


# ---------------------------- SEARCH ------------------------------- #
def search_data():
    site = web_in.get().title()
    try:
        with open("passwords.json", "r") as file:
            data_search = json.load(file)

    except FileNotFoundError:
        messagebox.showinfo(title="No Entry", message="There is no data to search from.")
    else:
        try:
            web_dict = data_search[site]
        except KeyError:
            messagebox.showinfo(title="Wrong Entry", message=f"No website saved by the the name '{site}'.")
        else:

            email_in.delete(0, END)
            email_in.insert(0, web_dict["email"])
            pass_in.delete(0, END)
            pass_in.insert(0, web_dict["password"])


# ---------------------------- UI SETUP ------------------------------- #

# Create the main window
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg=GRAY)

# Create canvas for logo display
canvas = Canvas(width=200, height=200, highlightthickness=0, bg=GRAY)
picture = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=picture)
canvas.grid(column=1, row=0)

# Labels and Entry fields for website, email, and password
website = Label(text="Website:", bg=GRAY, fg=WHITE)
website.grid(column=0, row=1)
user = Label(text="Email/Username:", bg=GRAY, fg=WHITE)
user.grid(column=0, row=2)
password = Label(text="Password:", bg=GRAY, fg=WHITE)
password.grid(column=0, row=3)

web_in = Entry(width=32, bg=BLACK, fg=WHITE)
web_in.focus()
web_in.grid(column=1, row=1, columnspan=1)
email_in = Entry(width=50, bg=BLACK, fg=WHITE)
email_in.insert(END, "esraelmekdem@gmail.com")
email_in.grid(column=1, row=2, columnspan=2)
pass_in = Entry(width=32, bg=BLACK, fg=WHITE)
pass_in.grid(column=1, row=3)

# Buttons for generating password and saving data
search = Button(text="search", width=14, bg=CYAN, command=search_data)
search.grid(column=2, row=1)
gen_pass = Button(text="Generate Password", bg=CYAN, command=generate_pass)
gen_pass.grid(column=2, row=3)
add = Button(text="Add", width=38, bg=CYAN, command=fetch_seq)
add.grid(column=1, row=4, columnspan=2)

# Run the application
window.mainloop()
