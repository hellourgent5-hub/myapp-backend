from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

users = {}

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if username in users:
        return jsonify({"success": False, "message": "User already exists"}), 400
    users[username] = password
    return jsonify({"success": True, "message": "Signup successful"})

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if users.get(username) == password:
        return jsonify({"success": True, "message": "Login successful"})
    return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.route("/logout", methods=["POST"])
def logout():
    return jsonify({"success": True, "message": "Logged out successfully"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
