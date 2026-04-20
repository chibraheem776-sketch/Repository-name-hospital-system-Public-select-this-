<<<<<<< HEAD
import sqlite3

conn = sqlite3.connect("hospital.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age TEXT,
    disease TEXT
)
""")

conn.commit()
conn.close()

=======
import sqlite3

conn = sqlite3.connect("hospital.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age TEXT,
    disease TEXT
)
""")

conn.commit()
conn.close()

>>>>>>> e720558b417703ce19a3714b049a1af65ef2da8f
print("Table created successfully!")