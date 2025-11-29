from flask import Blueprint, request, jsonify
import pymysql
import bcrypt

auth_bp = Blueprint("auth_bp", __name__)

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Md@123",
    "database": "healthydb",
    "charset": "utf8mb4"
}

def get_connection():
    return pymysql.connect(**DB_CONFIG)


@auth_bp.route("/login", methods=["POST"])
def login():
    conn = None
    cursor = None
    try:
        if not request.is_json:
            return jsonify({"success": False, "message": "Invalid request"}), 400

        data = request.json
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"success": False, "message": "Email and password required"}), 400

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, full_name, password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"success": False, "message": "Email not found"}), 404

        user_id, full_name, hashed_pw = user

        # Check password hash
        if not bcrypt.checkpw(password.encode("utf-8"), hashed_pw.encode("utf-8")):
            return jsonify({"success": False, "message": "Incorrect password"}), 401

        return jsonify({
            "success": True,
            "message": "Login successful",
            "user_id": user_id,
            "name": full_name
        })

    except Exception as e:
        print("❌ LOGIN ERROR:", e)
        return jsonify({"success": False, "message": "Server error"}), 500

    finally:
        if cursor: cursor.close()
        if conn: conn.close()
