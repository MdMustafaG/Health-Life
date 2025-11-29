from flask import Blueprint, render_template, request
import pymysql

appointment_bp = Blueprint("appointment", __name__, url_prefix="/appointment")

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="Md@123",
        database="healthydb",
        cursorclass=pymysql.cursors.DictCursor
    )

@appointment_bp.route("/", methods=["GET"])
def appointment():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT location FROM doctors ORDER BY location ASC")
        cities = [row["location"] for row in cursor.fetchall()]

        selected_city = request.args.get("city")
        if selected_city:
            cursor.execute("SELECT * FROM doctors WHERE location=%s ORDER BY created_at DESC", (selected_city,))
        else:
            cursor.execute("SELECT * FROM doctors ORDER BY created_at DESC")
        doctors = cursor.fetchall()
        for doc in doctors:
            if not doc.get("photo_path"):
                doc["photo_path"] = "default.jpg"
        return render_template("appointment.html", doctors=doctors, cities=cities, selected_city=selected_city)
    except Exception as e:
        print("Error in appointment:", e)
        return "Internal Server Error", 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
