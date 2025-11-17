import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
CORS(app)

DB_FILE = "users.db"

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            phone TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Add user
def add_user(username, email, phone, password):
    conn = sqlite3.connect(DB_FILE)
    try:
        hashed = generate_password_hash(password)
        conn.execute(
            "INSERT INTO users (username, email, phone, password) VALUES (?, ?, ?, ?)",
            (username, email, phone, hashed)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# Check login
def check_login(identifier, password):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(
        "SELECT password FROM users WHERE username=? OR email=? OR phone=?",
        (identifier, identifier, identifier)
    )
    row = cur.fetchone()
    conn.close()
    if row and check_password_hash(row[0], password):
        return True
    return False

# ----------------------------
# Routes
# ----------------------------
@app.route("/")
def home():
    return "Backend is running! Use /signup, /login, /logout endpoints."

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    phone = data.get("phone")
    password = data.get("password")
    if add_user(username, email, phone, password):
        return jsonify({"success": True, "message": "Signup successful"})
    return jsonify({"success": False, "message": "User already exists"}), 400

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    identifier = data.get("identifier")  # username, email, or phone
    password = data.get("password")
    if check_login(identifier, password):
        return jsonify({"success": True, "message": "Login successful"})
    return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.route("/logout", methods=["POST"])
def logout():
    return jsonify({"success": True, "message": "Logged out successfully"})

# ----------------------------
# Run app
# ----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
