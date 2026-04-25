from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secret123"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "hospital.db")

def get_db():
    return sqlite3.connect(db_path)

def create_tables():
    conn = get_db()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age TEXT,
        disease TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        doctor TEXT,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()

create_tables()

# INTRO
@app.route("/")
def intro():
    return render_template("intro.html")

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "1234":
            session["user"] = "admin"
            return redirect("/dashboard")
    return render_template("login.html")

# DASHBOARD
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    conn = get_db()
    c = conn.cursor()

    search = request.args.get("search")

    # search logic
    if search and search.strip() != "":
        c.execute("SELECT * FROM patients WHERE name LIKE ?", ('%' + search.strip() + '%',))
    else:
        c.execute("SELECT * FROM patients")

    patients = c.fetchall()

    # counts
    c.execute("SELECT COUNT(*) FROM patients")
    total = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM appointments")
    appointments_count = c.fetchone()[0]

    # 🔥 dynamic doctors count
    c.execute("SELECT COUNT(*) FROM doctors")
    doctors_count = c.fetchone()[0]

    conn.close()

    return render_template(
        "index.html",
        patients=patients,
        total=total,
        appointments_count=appointments_count,
        doctors_count=doctors_count
    )

# ADD PATIENT
@app.route("/add", methods=["POST"])
def add():
    conn = get_db()
    c = conn.cursor()

    c.execute("INSERT INTO patients (name, age, disease) VALUES (?, ?, ?)",
              (request.form["name"], request.form["age"], request.form["disease"]))

    conn.commit()
    conn.close()

    return redirect("/dashboard")

# VIEW
@app.route("/view/<int:id>")
def view(id):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM patients WHERE id=?", (id,))
    patient = c.fetchone()
    conn.close()
    return render_template("view.html", p=patient)

# EDIT
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = get_db()
    c = conn.cursor()

    if request.method == "POST":
        c.execute("""
        UPDATE patients
        SET name=?, age=?, disease=?
        WHERE id=?
        """, (
            request.form["name"],
            request.form["age"],
            request.form["disease"],
            id
        ))
        conn.commit()
        conn.close()
        return redirect("/dashboard")

    c.execute("SELECT * FROM patients WHERE id=?", (id,))
    patient = c.fetchone()
    conn.close()

    return render_template("edit.html", p=patient)

# DELETE
@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM patients WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/dashboard")

# APPOINTMENTS
@app.route("/appointments", methods=["GET", "POST"])
def appointments():
    conn = get_db()
    c = conn.cursor()

    if request.method == "POST":
        c.execute("INSERT INTO appointments (patient_name, doctor, date) VALUES (?, ?, ?)",
                  (request.form["patient"], request.form["doctor"], request.form["date"]))
        conn.commit()

    c.execute("SELECT * FROM appointments")
    data = c.fetchall()

    conn.close()
    return render_template("appointments.html", data=data)

# DOCTORS
@app.route("/doctors", methods=["GET", "POST"])
def doctors():
    conn = get_db()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        specialty TEXT
    )
    """)

    if request.method == "POST":
        c.execute("INSERT INTO doctors (name, specialty) VALUES (?, ?)",
                  (request.form["name"], request.form["specialty"]))
        conn.commit()

    c.execute("SELECT * FROM doctors")
    data = c.fetchall()

    conn.close()

    return render_template("doctors.html", data=data)

# ADMIN
@app.route("/admin")
def admin():
    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM patients")
    total_patients = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM appointments")
    total_appointments = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM doctors")
    total_doctors = c.fetchone()[0]

    conn.close()

    return render_template("admin.html",
                           patients=total_patients,
                           appointments=total_appointments,
                           doctors=total_doctors)

# LOGOUT
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)