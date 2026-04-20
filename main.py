<<<<<<< HEAD
import json

try:
    with open("patients.json", "r") as f:
        patients = json.load(f)
except:
    patients = []

def save_data():
    with open("patients.json", "w") as f:
        json.dump(patients, f)

def add_patient():
    name = input("Enter patient name: ")
    age = input("Enter age: ")
    disease = input("Enter disease: ")

    patient = {
        "name": name,
        "age": age,
        "disease": disease
    }

    patients.append(patient)
    save_data()
    print("Patient added successfully!\n")

def view_patients():
    if len(patients) == 0:
        print("No patients found\n")
        return

    for i, p in enumerate(patients):
        print(f"{i+1}. {p['name']} | Age: {p['age']} | Disease: {p['disease']}")
    print()

def search_patient():
    name = input("Enter name to search: ")
    for p in patients:
        if p["name"].lower() == name.lower():
            print(p)
            return
    print("Not found\n")

def delete_patient():
    name = input("Enter name to delete: ")
    for p in patients:
        if p["name"].lower() == name.lower():
            patients.remove(p)
            save_data()
            print("Deleted\n")
            return
    print("Not found\n")

while True:
    print("1. Add Patient")
    print("2. View Patients")
    print("3. Search Patient")
    print("4. Delete Patient")
    print("5. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        add_patient()
    elif choice == "2":
        view_patients()
    elif choice == "3":
        search_patient()
    elif choice == "4":
        delete_patient()
    elif choice == "5":
        break
    else:
=======
import json

try:
    with open("patients.json", "r") as f:
        patients = json.load(f)
except:
    patients = []

def save_data():
    with open("patients.json", "w") as f:
        json.dump(patients, f)

def add_patient():
    name = input("Enter patient name: ")
    age = input("Enter age: ")
    disease = input("Enter disease: ")

    patient = {
        "name": name,
        "age": age,
        "disease": disease
    }

    patients.append(patient)
    save_data()
    print("Patient added successfully!\n")

def view_patients():
    if len(patients) == 0:
        print("No patients found\n")
        return

    for i, p in enumerate(patients):
        print(f"{i+1}. {p['name']} | Age: {p['age']} | Disease: {p['disease']}")
    print()

def search_patient():
    name = input("Enter name to search: ")
    for p in patients:
        if p["name"].lower() == name.lower():
            print(p)
            return
    print("Not found\n")

def delete_patient():
    name = input("Enter name to delete: ")
    for p in patients:
        if p["name"].lower() == name.lower():
            patients.remove(p)
            save_data()
            print("Deleted\n")
            return
    print("Not found\n")

while True:
    print("1. Add Patient")
    print("2. View Patients")
    print("3. Search Patient")
    print("4. Delete Patient")
    print("5. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        add_patient()
    elif choice == "2":
        view_patients()
    elif choice == "3":
        search_patient()
    elif choice == "4":
        delete_patient()
    elif choice == "5":
        break
    else:
>>>>>>> e720558b417703ce19a3714b049a1af65ef2da8f
        print("Invalid choice\n")