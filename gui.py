<<<<<<< HEAD
import tkinter as tk
from tkinter import messagebox
import json

# Load data
try:
    with open("patients.json", "r") as f:
        patients = json.load(f)
except:
    patients = []

def save_data():
    with open("patients.json", "w") as f:
        json.dump(patients, f)

def add_patient():
    name = name_entry.get()
    age = age_entry.get()
    disease = disease_entry.get()

    if name == "" or age == "" or disease == "":
        messagebox.showerror("Error", "All fields required")
        return

    patient = {"name": name, "age": age, "disease": disease}
    patients.append(patient)
    save_data()

    messagebox.showinfo("Success", "Patient Added")

    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    disease_entry.delete(0, tk.END)

def view_patients():
    listbox.delete(0, tk.END)
    for p in patients:
        listbox.insert(tk.END, f"{p['name']} | {p['age']} | {p['disease']}")

# UI
root = tk.Tk()
root.title("Hospital System")

tk.Label(root, text="Name").pack()
name_entry = tk.Entry(root)
name_entry.pack()

tk.Label(root, text="Age").pack()
age_entry = tk.Entry(root)
age_entry.pack()

tk.Label(root, text="Disease").pack()
disease_entry = tk.Entry(root)
disease_entry.pack()

tk.Button(root, text="Add Patient", command=add_patient).pack()
tk.Button(root, text="View Patients", command=view_patients).pack()

listbox = tk.Listbox(root, width=50)
listbox.pack()

=======
import tkinter as tk
from tkinter import messagebox
import json

# Load data
try:
    with open("patients.json", "r") as f:
        patients = json.load(f)
except:
    patients = []

def save_data():
    with open("patients.json", "w") as f:
        json.dump(patients, f)

def add_patient():
    name = name_entry.get()
    age = age_entry.get()
    disease = disease_entry.get()

    if name == "" or age == "" or disease == "":
        messagebox.showerror("Error", "All fields required")
        return

    patient = {"name": name, "age": age, "disease": disease}
    patients.append(patient)
    save_data()

    messagebox.showinfo("Success", "Patient Added")

    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    disease_entry.delete(0, tk.END)

def view_patients():
    listbox.delete(0, tk.END)
    for p in patients:
        listbox.insert(tk.END, f"{p['name']} | {p['age']} | {p['disease']}")

# UI
root = tk.Tk()
root.title("Hospital System")

tk.Label(root, text="Name").pack()
name_entry = tk.Entry(root)
name_entry.pack()

tk.Label(root, text="Age").pack()
age_entry = tk.Entry(root)
age_entry.pack()

tk.Label(root, text="Disease").pack()
disease_entry = tk.Entry(root)
disease_entry.pack()

tk.Button(root, text="Add Patient", command=add_patient).pack()
tk.Button(root, text="View Patients", command=view_patients).pack()

listbox = tk.Listbox(root, width=50)
listbox.pack()

>>>>>>> e720558b417703ce19a3714b049a1af65ef2da8f
root.mainloop()