from tkinter import *
from tkinter import messagebox
import random
import pyperclip

BLACK = "#222831"
GRAY = "#31363F"
CYAN = "#76ABAE"
WHITE = "#EEEEEE"

lower_letters = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
]
upper_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_pass():
    pass_in.delete(0, END)
    lr_letters = random.randint(5, 7)
    up_letters = random.randint(3, 5)
    nr_numbers = random.randint(2, 6)
    nr_symbols = random.randint(1, 4)

    code1 = [random.choice(lower_letters) for i in range(0, up_letters)]
    code2 = [random.choice(upper_letters) for i in range(0, lr_letters)]
    code3 = [random.choice(symbols) for i in range(0, nr_symbols)]
    code4 = [random.choice(numbers) for i in range(0, nr_numbers)]

    # Convert the strings to a list after contacting them.
    list_code = code1 + code2 + code3 + code4
    # shuffle through the list 3 times because I like it.
    random.shuffle(list_code)
    random.shuffle(list_code)
    random.shuffle(list_code)
    # Convert the list to a string that gets displayed to the user.
    shuffled_passcode = "".join(list_code)
    pass_in.insert(END, shuffled_passcode)
    pyperclip.copy(shuffled_passcode)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def fetch_seq():
    web = web_in.get().title()
    email = email_in.get()
    passw = pass_in.get()

    if len(web) > 0 and len(email) > 0:
        if len(passw) > 8:
            is_ok = messagebox.askokcancel(title=web, message=f"The information entered are:\n"
                                                              f"Email: {email}\n"
                                                              f"Password: {passw}\n"
                                                              f"Is it correct")
            if is_ok:
                style = f"{web} | {email} | {passw}\n"
                with open("passwords.txt", "a") as file:
                    file.write(style)
                    messagebox.showinfo(title=web, message="Save successful")
                    web_in.delete(0, END)
                    pass_in.delete(0, END)

        else:
            messagebox.showwarning(title="Weak Password", message=f"inputted password needs a minimum of 8 characters\n "
                                                                  f"current length: {len(passw)}")
    else:
        messagebox.showwarning(title="Oops", message="Please don't leave any field empty!")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg=GRAY)

canvas = Canvas(width=200, height=200, highlightthickness=0, bg=GRAY)
picture = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=picture)
canvas.grid(column=1, row=0)

website = Label(text="Website:", bg=GRAY, fg=WHITE)
website.grid(column=0, row=1)

user = Label(text="Email/Username:", bg=GRAY, fg=WHITE)
user.grid(column=0, row=2)

password = Label(text="Password:", bg=GRAY, fg=WHITE)
password.grid(column=0, row=3)

web_in = Entry(width=50, bg=BLACK, fg=WHITE)
web_in.focus()
web_in.grid(column=1, row=1, columnspan=2)

email_in = Entry(width=50, bg=BLACK, fg=WHITE)
email_in.insert(END, "esraelmekdem@gmail.com")
email_in.grid(column=1, row=2, columnspan=2)

pass_in = Entry(width=32, bg=BLACK, fg=WHITE)
pass_in.grid(column=1, row=3)

gen_pass = Button(text="Generate Password", bg=CYAN, command=generate_pass)
gen_pass.grid(column=2, row=3)

add = Button(text="Add", width=38, bg=CYAN, command=fetch_seq)
add.grid(column=1, row=4, columnspan=2)

window.mainloop()
