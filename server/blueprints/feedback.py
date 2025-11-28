from flask import Blueprint, request, jsonify, render_template
import pymysql
from datetime import datetime

feedback_bp = Blueprint("feedback_bp", __name__)

# MySQL Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "attar",
    "password": "Attar@2025",
    "database": "healthydb",
    "charset": "utf8mb4"
}

def get_connection():
    return pymysql.connect(**DB_CONFIG)

# Route to submit feedback
@feedback_bp.route("/submit_feedback", methods=["POST"])
def submit_feedback():
    data = request.get_json()
    username = data.get("username")
    rating = data.get("rating")
    review = data.get("review")

    if not username or not rating or not review:
        return jsonify({"success": False, "message": "Invalid data"})

    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO feedback (username, rating, review, created_at) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (username, rating, review, datetime.now()))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"success": True})
    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": "Database error"})

# Route to view all feedback (admin)
@feedback_bp.route("/admin_reviews")
def admin_reviews():
    try:
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM feedback ORDER BY created_at DESC")
        feedbacks = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template("admin_reviews.html", feedbacks=feedbacks)
    except Exception as e:
        print(e)
        return "Database connection error"
