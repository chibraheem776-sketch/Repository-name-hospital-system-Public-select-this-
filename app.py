from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# DATABASE CONNECT
def get_db():
    conn = sqlite3.connect("hospital.db")
    conn.row_factory = sqlite3.Row
    return conn

# ================= HOME =================
@app.route('/')
def home():
    if "user" not in session:
        return redirect("/login")

    conn = get_db()
    patients = conn.execute("SELECT * FROM patients").fetchall()
    conn.close()

    return render_template("index.html", patients=patients, total=len(patients))


# ================= LOGIN =================
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["user"] = request.form["username"]
        return redirect("/")
    return render_template("login.html")


# ================= LOGOUT =================
@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect("/login")


# ================= ADD PATIENT =================
@app.route('/add', methods=["POST"])
def add():
    name = request.form["name"]
    age = request.form["age"]
    disease = request.form["disease"]

    conn = get_db()
    conn.execute("INSERT INTO patients (name, age, disease) VALUES (?, ?, ?)",
                 (name, age, disease))
    conn.commit()
    conn.close()

    return redirect("/")


# ================= DELETE =================
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM patients WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")


# ================= EDIT =================
@app.route('/edit/<int:id>', methods=["GET", "POST"])
def edit(id):
    conn = get_db()

    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        disease = request.form["disease"]

        conn.execute("UPDATE patients SET name=?, age=?, disease=? WHERE id=?",
                     (name, age, disease, id))
        conn.commit()
        conn.close()
        return redirect("/")

    patient = conn.execute("SELECT * FROM patients WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("edit.html", patient=patient)


# ================= VIEW =================
@app.route('/view/<int:id>')
def view(id):
    conn = get_db()
    patient = conn.execute("SELECT * FROM patients WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("view.html", patient=patient)


# ================= DOCTORS =================
@app.route('/doctors')
def doctors():
    return render_template("doctors.html")


# ================= APPOINTMENTS =================
@app.route('/appointments')
def appointments():
    return render_template("appointments.html")


# ================= ADMIN =================
@app.route('/admin')
def admin():
    return render_template("admin.html")


# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)