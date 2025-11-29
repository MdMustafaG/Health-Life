from flask import Blueprint, request, jsonify
import pymysql
import bcrypt

signup_bp = Blueprint("signup_bp", __name__)

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Md@123",
    "database": "healthydb",
    "charset": "utf8mb4"
}

def get_connection():
    return pymysql.connect(**DB_CONFIG)


@signup_bp.route("/signup", methods=["POST"])
def signup():
    conn = None
    cursor = None
    try:
        data = request.json
        full_name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if not full_name or not email or not password:
            return jsonify({"success": False, "message": "All fields required"}), 400

        # Hash password
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        conn = get_connection()
        cursor = conn.cursor()

        # Check duplicate email
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({"success": False, "message": "Email already registered"}), 409

        # Insert user
        cursor.execute("""
            INSERT INTO users (full_name, email, password)
            VALUES (%s, %s, %s)
        """, (full_name, email, hashed_pw.decode("utf-8")))

        conn.commit()

        return jsonify({"success": True, "message": "Signup successful!"})

    except Exception as e:
        print("❌ SIGNUP ERROR:", e)
        return jsonify({"success": False, "message": "Server error"}), 500

    finally:
        if cursor: cursor.close()
        if conn: conn.close()
