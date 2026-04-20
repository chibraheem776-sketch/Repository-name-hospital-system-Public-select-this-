import tkinter as tk
from tkinter import messagebox
import os

def login():
    username = user_entry.get()
    password = pass_entry.get()

    if username == "admin" and password == "1234":
        messagebox.showinfo("Success", "Login Successful")
        root.destroy()
        os.system("py gui.py")  # open main app
    else:
        messagebox.showerror("Error", "Invalid credentials")

root = tk.Tk()
root.title("Login System")

tk.Label(root, text="Username").pack()
user_entry = tk.Entry(root)
user_entry.pack()

tk.Label(root, text="Password").pack()
pass_entry = tk.Entry(root, show="*")
pass_entry.pack()

tk.Button(root, text="Login", command=login).pack()

root.mainloop()