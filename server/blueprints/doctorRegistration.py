from flask import Blueprint, request, jsonify, send_from_directory
import pymysql, os
from datetime import datetime
from werkzeug.utils import secure_filename
import uuid

doctor_bp = Blueprint("doctor_bp", __name__)

#  DATABASE Configaration 
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Md@123",
    "database": "healthydb",
    "charset": "utf8mb4"
}

def get_connection():
    return pymysql.connect(**DB_CONFIG)


# IMAGE UPLOAD 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "..", "doctors_upload_images")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXT = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT


# Route uploaded images
@doctor_bp.route('/doctor_image/<filename>')
def doctor_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


# Route Doctor register
@doctor_bp.route("/register_doctor", methods=["POST"])
def register_doctor():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        name = request.form.get("name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        experience = request.form.get("experience")
        specialization = request.form.get("specialization")
        services = request.form.get("services")  
        clinic = request.form.get("clinic")
        location = request.form.get("location")
        photo = request.files.get("photo")

        if not all([name, phone, email, specialization, photo]):
            return jsonify({"success": False, "message": "Missing required fields"}), 400

        if not allowed_file(photo.filename):
            return jsonify({"success": False, "message": "Invalid file type"}), 400

        # Check duplicate email
        cursor.execute("SELECT id FROM doctors WHERE email=%s", (email,))
        if cursor.fetchone():
            return jsonify({"success": False, "message": "Email already registered"}), 409

        # Save uploaded image with unique filenames
        ext = photo.filename.rsplit(".", 1)[1].lower()
        unique_name = f"{uuid.uuid4().hex}.{ext}"     
        filename = secure_filename(unique_name)

        file_path = os.path.join(UPLOAD_FOLDER, filename)
        photo.save(file_path)

        # Insert database record
        sql = """
            INSERT INTO doctors
            (name, phone, email, experience, specialization, services, clinic, location, photo_path, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (name, phone, email, experience, specialization, services,
                  clinic, location, filename, datetime.utcnow())

        cursor.execute(sql, values)
        conn.commit()

        return jsonify({"success": True, "message": "Doctor registered successfully."})

    except Exception as e:
        print("❌ Error in register_doctor:", e)
        return jsonify({"success": False, "message": "Server error"}), 500

    finally:
        cursor.close()
        conn.close()


# FETCH ALL DOCTORS 
@doctor_bp.route("/get_doctors", methods=["GET"])
def get_doctors():
    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    try:
        cursor.execute("""
            SELECT id, name, specialization, photo_path, clinic, location
            FROM doctors ORDER BY created_at DESC
        """)
        doctors = cursor.fetchall()

        # Add image fallback
        for doctor in doctors:
            if not doctor.get("photo_path"):
                doctor["photo_path"] = "default.jpg"

        return jsonify({"success": True, "doctors": doctors})

    except Exception as e:
        print("❌ Error in get_doctors:", e)
        return jsonify({"success": False, "message": "Server error"}), 500

    finally:
        cursor.close()
        conn.close()
