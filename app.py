import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# ---------------------------
# Initialize database
# ---------------------------
DB_FILE = "users.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)"
    )
    conn.commit()
    conn.close()

init_db()

# ---------------------------
# Helper functions
# ---------------------------
def add_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    try:
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)", (username, password)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def check_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    return row and row[0] == password

# ---------------------------
# Routes
# ---------------------------
@app.route("/")
def home():
    return "Backend is running! Use /signup, /login, /logout endpoints."

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if add_user(username, password):
        return jsonify({"success": True, "message": "Signup successful"})
    return jsonify({"success": False, "message": "User already exists"}), 400

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if check_user(username, password):
        return jsonify({"success": True, "message": "Login successful"})
    return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.route("/logout", methods=["POST"])
def logout():
    return jsonify({"success": True, "message": "Logged out successfully"})

# ---------------------------
# Run app
# ---------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
