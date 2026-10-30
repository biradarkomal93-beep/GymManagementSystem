from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
def init_db():
    conn = sqlite3.connect("gym.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT,
            phone TEXT,
            email TEXT,
            age INTEGER,
            gender TEXT,
            membership TEXT
        )
    """)

    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        full_name = request.form.get("full_name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        age = request.form.get("age")
        gender = request.form.get("gender")
        membership = request.form.get("membership")

        conn = sqlite3.connect("gym.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO members
            (full_name, phone, email, age, gender, membership)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (full_name, phone, email, age, gender, membership))

        conn.commit()
        conn.close()

        return """
        <h2>Registration Successful!</h2>
        <p>Welcome to FITZONE GYM!</p>
        <a href="/">Go to Home</a>
        """

    return render_template("register.html")

@app.route("/admin")
def admin():
    conn = sqlite3.connect("gym.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()

    conn.close()

    return render_template("admin.html", members=members)
if __name__ == "__main__":
    init_db()
    app.run(debug=True)