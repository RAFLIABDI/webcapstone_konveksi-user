from flask import Blueprint, request, jsonify
from models.database import mongo

auth_bp = Blueprint("auth", __name__)

# =========================
# REGISTER
# =========================
@auth_bp.route("/api/register", methods=["POST"])
def register():

    data = request.get_json()

    print("========== REGISTER ==========")
    print(data)

    nama = data.get("nama")
    email = data.get("email")
    password = data.get("password")

    mongo.db.users.insert_one({
        "nama": nama,
        "email": email,
        "password": password
    })

    print("USER BERHASIL DISIMPAN")

    return jsonify({
        "success": True,
        "message": "Register berhasil"
    })

# =========================
# LOGIN
# =========================
@auth_bp.route("/api/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = mongo.db.users.find_one({
        "email": email,
        "password": password
    })

    if not user:
        return jsonify({
            "success": False,
            "message": "Email atau password salah"
        })

    return jsonify({
        "success": True,
        "user": {
            "nama": user["nama"],
            "email": user["email"]
        }
    })