from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
try:
    with open("default_user.json", "r") as default_user:
        data = json.load(default_user)
        DEFAULT_USERNAME = data["default username"]
except FileNotFoundError:
    with open("default_user.json", "w") as default_user:
        data = {"default username": ""}
        DEFAULT_USERNAME = data["default username"]
        json.dump(data, default_user)


# ---------------------------- SEARCH MECHANISM ------------------------------- #
def search():
    website_name = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            contents = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="You haven't saved any Usernames or Passwords yet!")
    except json.decoder.JSONDecodeError:
        messagebox.showerror(title="Error", message="Your list is empty")
    else:
        if len(website_name) == 0:
            messagebox.showinfo(title="Error", message="Please don't leave Website field empty!")
        elif website_name in contents:
            for (key, value) in contents.items():
                if website_name == key:
                    messagebox.showinfo(title=f"{website_name}", message=f"Username: {value['username']}\nPassword: "
                                                                         f"{value['password']}")
                    pyperclip.copy(value["password"])
        elif contents == {}:
            messagebox.showerror(title="Error", message="Your list is empty")
        else:
            messagebox.showerror(title="Error", message="Website not found!")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = [random.choice(letters) for letter in range(nr_letters)]
    password_list += [random.choice(symbols) for symbol in range(nr_symbols)]
    password_list += [random.choice(numbers) for number in range(nr_numbers)]
    random.shuffle(password_list)

    password = "".join(password_list)

    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    global DEFAULT_USERNAME
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "username": username,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Error", message="Please don't leave any fields empty!")

    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nUsername: {username}"
                                                              f" \nPassword: {password} \nIs it ok to save?")
        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    # Reading old data
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            except json.decoder.JSONDecodeError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                # Updating old data with new data
                data.update(new_data)
                with open("data.json", "w") as data_file:
                    # Saving the updated data
                    json.dump(data, data_file, indent=4)

        pyperclip.copy(f"{password}")
        website_entry.delete(0, END)
        password_entry.delete(0, END)
        website_entry.focus()
        if username != DEFAULT_USERNAME:
            changing_username_is_ok = messagebox.askokcancel(title="Changing default username", message=f"Do you want"
                                                                                                        f" to save "
                                                                                                        f"{username} "
                                                                                                        f"as the "
                                                                                                        f"default "
                                                                                                        f"username?")
            if changing_username_is_ok:
                username_entry.delete(0, END)
                username_entry.insert(0, username)
                new_default_username = {"default username": username}
                with open("default_user.json", "r") as old_username:
                    old_data = json.load(old_username)
                old_data.update(new_default_username)
                with open("default_user.json", "w") as new_username:
                    json.dump(old_data, new_username)
            else:
                username_entry.delete(0, END)
                username_entry.insert(0, DEFAULT_USERNAME)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def delete():
    website_name = website_entry.get()
    if len(website_name) == 0:
        messagebox.showinfo(title="Error", message="Please don't leave Website field empty!")
    else:
        try:
            with open("data.json", "r") as data_file:
                contents = json.load(data_file)
        except FileNotFoundError:
            messagebox.showerror(title="Error", message="You haven't saved any Usernames or Passwords yet!")
        else:
            if website_name in contents:
                is_ok = messagebox.askokcancel(title=f"Delete {website_name}", message=f"Are you sure you want to"
                                                                                       f" permanently delete "
                                                                                       f"{website_name} with its "
                                                                                       f"Username and Password?")
                if is_ok:
                    contents[website_name].pop("username")
                    contents[website_name].pop("password")
                    delete_website_name = contents.pop(website_name)
                    contents.update(delete_website_name)
                    with open("data.json", "w") as data_to_delete:
                        json.dump(contents, data_to_delete, indent=4)
                        messagebox.showinfo(title="Info", message=f"{website_name} has been deleted")
            else:
                messagebox.showerror(title="Error", message="Website not found!")


# ---------------------------- ACCOUNTS LIST ------------------------------- #
def accounts():
    try:
        with open("data.json", "r") as data_file:
            contents = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="You haven't saved any Usernames or Passwords yet!")
    except json.decoder.JSONDecodeError:
        messagebox.showerror(title="Error", message="Your list is empty")
    else:
        if contents == {}:
            messagebox.showerror(title="Error", message="Your list is empty")
        else:
            accounts_list = [key for (key, value) in contents.items()]
            show_accounts = '\n'.join(accounts_list)
            messagebox.showinfo(title="Accounts", message=f"{show_accounts}")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_png = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_png)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:", padx=3, pady=3)
website_label.grid(column=0, row=1)
username_label = Label(text="Email/Username:", padx=3, pady=3)
username_label.grid(column=0, row=2)
password_label = Label(text="Password:", padx=3, pady=3)
password_label.grid(column=0, row=3)

# Entries
website_entry = Entry(width=33)
website_entry.grid(column=1, row=1)
website_entry.focus()
username_entry = Entry(width=52)
username_entry.grid(column=1, row=2, columnspan=2)
username_entry.insert(0, DEFAULT_USERNAME)
password_entry = Entry(width=33)
password_entry.grid(column=1, row=3)

# Buttons
search_button = Button(text="Search", width=14, command=search)
search_button.grid(column=2, row=1)
generate_button = Button(text="Generate Password", command=generate_password, width=14)
generate_button.grid(column=2, row=3)
add_button = Button(text="Add", width=44, command=save)
add_button.grid(column=1, row=4, columnspan=2)
delete_button = Button(text="Delete", width=44, command=delete)
delete_button.grid(column=1, row=5, columnspan=2)
list_button = Button(text="Accounts", width=44, command=accounts)
list_button.grid(column=1, row=6, columnspan=2)

window.mainloop()