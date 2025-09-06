from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
CORS(app)

# Absolute path to DB
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "careerrec.db")

# Signup route
@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get("fullName")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    password_hash = generate_password_hash(password)

    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                    (name, email, password_hash))
        conn.commit()
        conn.close()
        return jsonify({"message": "Signup successful"}), 200
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already registered"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Signup GET route (for testing in browser)
@app.route('/api/signup', methods=['GET'])
def signup_info():
    return jsonify({"message": "Signup endpoint is working. Use POST to create an account."}), 200


# Login route
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400

    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT id, name, email, password_hash FROM users WHERE email = ?", (email,))
        user = cur.fetchone()
        conn.close()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    if user and check_password_hash(user[3], password):
        return jsonify({
            "message": "Login successful",
            "user": {"id": user[0], "name": user[1], "email": user[2]}
        }), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401

# ✅ Login GET route (for testing in browser)
@app.route('/api/login', methods=['GET'])
def login_info():
    return jsonify({"message": "Login endpoint is working. Use POST with email & password."}), 200


# ✅ Optional root route (just to test server is alive)
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Flask server is running 🚀"}), 200



if __name__ == "_main_":
    app.run(debug=True)