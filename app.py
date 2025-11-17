from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

# -------------------------
# Database setup
# -------------------------
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# -------------------------
# Signup
# -------------------------
@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    phone = data.get("phone")
    password = data.get("password")

    if not all([username, email, phone, password]):
        return jsonify({"success": False, "message": "All fields are required"}), 400

    hashed_password = generate_password_hash(password)

    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('INSERT INTO users (username, email, phone, password) VALUES (?, ?, ?, ?)',
                  (username, email, phone, hashed_password))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Signup successful"})
    except sqlite3.IntegrityError:
        return jsonify({"success": False, "message": "Email or phone already exists"}), 400

# -------------------------
# Login
# -------------------------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    identifier = data.get("identifier")  # email or phone
    password = data.get("password")

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT username, password FROM users WHERE email=? OR phone=?', (identifier, identifier))
    user = c.fetchone()
    conn.close()

    if user and check_password_hash(user[1], password):
        return jsonify({"success": True, "message": f"Login successful. Welcome {user[0]}!"})
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

# -------------------------
# Logout
# -------------------------
@app.route("/logout", methods=["POST"])
def logout():
    return jsonify({"success": True, "message": "Logged out successfully"})

# -------------------------
# Run app
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
