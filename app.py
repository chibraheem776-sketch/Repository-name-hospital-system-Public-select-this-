from flask import Flask, render_template, request, redirect, session, send_file
import sqlite3
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from fpdf import FPDF

app = Flask(__name__)
app.secret_key = "secret123"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "hospital.db")

def get_db():
    return sqlite3.connect(db_path)

# ================= CREATE TABLES =================
def create_tables():
    conn = get_db()
    c = conn.cursor()

    # patients table
    c.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age TEXT,
        disease TEXT
    )
    """)

    # appointments table (NEW)
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

# ================= LOGIN =================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "1234":
            session["user"] = "admin"
            return redirect("/dashboard")
    return render_template("login.html")

# ================= DASHBOARD =================
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    conn = get_db()
    c = conn.cursor()

    search = request.args.get("search")

    if search:
        c.execute("SELECT * FROM patients WHERE name LIKE ?", ('%' + search + '%',))
    else:
        c.execute("SELECT * FROM patients")

    patients = c.fetchall()

    c.execute("SELECT COUNT(*) FROM patients")
    total = c.fetchone()[0]

    # chart
    diseases = {}
    for p in patients:
        diseases[p[3]] = diseases.get(p[3], 0) + 1

    if diseases:
        plt.clf()
        plt.bar(diseases.keys(), diseases.values())

        chart_path = os.path.join(BASE_DIR, "static", "chart.png")
        plt.savefig(chart_path)
        plt.close()

    conn.close()

    return render_template("index.html", patients=patients, total=total)

# ================= ADD PATIENT =================
@app.route("/add", methods=["POST"])
def add():
    conn = get_db()
    c = conn.cursor()

    c.execute("INSERT INTO patients (name, age, disease) VALUES (?, ?, ?)",
              (request.form["name"], request.form["age"], request.form["disease"]))

    conn.commit()
    conn.close()

    return redirect("/dashboard")

# ================= VIEW =================
@app.route("/view/<int:id>")
def view(id):
    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT * FROM patients WHERE id=?", (id,))
    patient = c.fetchone()

    conn.close()

    return render_template("view.html", p=patient)

# ================= EDIT =================
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

# ================= DELETE =================
@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    c = conn.cursor()

    c.execute("DELETE FROM patients WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/dashboard")

# ================= REPORT =================
@app.route("/report")
def report():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM patients")
    data = c.fetchall()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for p in data:
        pdf.cell(200, 10, txt=f"{p[1]} | {p[2]} | {p[3]}", ln=True)

    file_path = os.path.join(BASE_DIR, "report.pdf")
    pdf.output(file_path)

    return send_file(file_path, as_attachment=True)

# ================= DOCTORS PAGE =================
@app.route("/doctors")
def doctors():
    return render_template("doctors.html")

# ================= APPOINTMENTS =================
from flask import Flask, render_template, request, redirect, session, send_file
import sqlite3
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from fpdf import FPDF

app = Flask(__name__)
app.secret_key = "secret123"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "hospital.db")

def get_db():
    return sqlite3.connect(db_path)

# ================= CREATE TABLES =================
def create_tables():
    conn = get_db()
    c = conn.cursor()

    # patients table
    c.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age TEXT,
        disease TEXT
    )
    """)

    # appointments table (NEW)
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

# ================= LOGIN =================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "1234":
            session["user"] = "admin"
            return redirect("/dashboard")
    return render_template("login.html")

# ================= DASHBOARD =================
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    conn = get_db()
    c = conn.cursor()

    search = request.args.get("search")

    if search:
        c.execute("SELECT * FROM patients WHERE name LIKE ?", ('%' + search + '%',))
    else:
        c.execute("SELECT * FROM patients")

    patients = c.fetchall()

    c.execute("SELECT COUNT(*) FROM patients")
    total = c.fetchone()[0]

    # chart
    diseases = {}
    for p in patients:
        diseases[p[3]] = diseases.get(p[3], 0) + 1

    if diseases:
        plt.clf()
        plt.bar(diseases.keys(), diseases.values())

        chart_path = os.path.join(BASE_DIR, "static", "chart.png")
        plt.savefig(chart_path)
        plt.close()

    conn.close()

    return render_template("index.html", patients=patients, total=total)

# ================= ADD PATIENT =================
@app.route("/add", methods=["POST"])
def add():
    conn = get_db()
    c = conn.cursor()

    c.execute("INSERT INTO patients (name, age, disease) VALUES (?, ?, ?)",
              (request.form["name"], request.form["age"], request.form["disease"]))

    conn.commit()
    conn.close()

    return redirect("/dashboard")

# ================= VIEW =================
@app.route("/view/<int:id>")
def view(id):
    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT * FROM patients WHERE id=?", (id,))
    patient = c.fetchone()

    conn.close()

    return render_template("view.html", p=patient)

# ================= EDIT =================
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

# ================= DELETE =================
@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    c = conn.cursor()

    c.execute("DELETE FROM patients WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/dashboard")

# ================= REPORT =================
@app.route("/report")
def report():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM patients")
    data = c.fetchall()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for p in data:
        pdf.cell(200, 10, txt=f"{p[1]} | {p[2]} | {p[3]}", ln=True)

    file_path = os.path.join(BASE_DIR, "report.pdf")
    pdf.output(file_path)

    return send_file(file_path, as_attachment=True)

# ================= DOCTORS PAGE =================
@app.route("/doctors")
def doctors():
    return render_template("doctors.html")

# ================= APPOINTMENTS =================
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

# ================= ADMIN =================
@app.route("/admin")
def admin():
    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM patients")
    total_patients = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM appointments")
    total_appointments = c.fetchone()[0]

    conn.close()

    return render_template("admin.html",
                           patients=total_patients,
                           appointments=total_appointments)

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)

# ================= ADMIN =================
@app.route("/admin")
def admin():
    if "user" not in session:
        return redirect("/")

    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM patients")
    total_patients = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM appointments")
    total_appointments = c.fetchone()[0]

    doctors = 5   # 👈 ADD THIS LINE

    conn.close()

    return render_template("admin.html",
                           patients=total_patients,
                           appointments=total_appointments,
                           doctors=doctors)

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)