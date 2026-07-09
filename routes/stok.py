from flask import Blueprint, jsonify, request
from bson.objectid import ObjectId
from models.database import mongo

stok_bp = Blueprint("stok", __name__)

# ==========================
# GET ALL STOK
# ==========================
@stok_bp.route("/api/stok", methods=["GET"])
def get_stok():

    data = []

    stok = mongo.db.stok.find()

    for item in stok:

        data.append({

            "_id": str(item["_id"]),

            "nama": item.get("nama"),

            "kategori": item.get("kategori"),

            "stok": item.get("stok"),

            "minimal": item.get("minimal"),

            "status": item.get("status"),

            "satuan": item.get("satuan")

        })

    return jsonify({
        "success": True,
        "data": data
    })


# ==========================
# TAMBAH STOK
# ==========================
@stok_bp.route("/api/stok", methods=["POST"])
def tambah_stok():

    data = request.get_json()

    mongo.db.stok.insert_one({

        "nama": data["nama"],

        "kategori": data["kategori"],

        "stok": int(data["stok"]),

        "minimal": int(data["minimal"]),

        "status": data["status"],

        "satuan": data["satuan"]

    })

    return jsonify({

        "success": True,

        "message": "Stok berhasil ditambahkan"

    })


# ==========================
# UPDATE STOK
# ==========================
@stok_bp.route("/api/stok/<id>", methods=["PUT"])
def update_stok(id):

    data = request.get_json()

    mongo.db.stok.update_one(

        {

            "_id": ObjectId(id)

        },

        {

            "$set": {

                "nama": data["nama"],

                "kategori": data["kategori"],

                "stok": int(data["stok"]),

                "minimal": int(data["minimal"]),

                "status": data["status"],

                "satuan": data["satuan"]

            }

        }

    )

    return jsonify({

        "success": True,

        "message": "Data berhasil diupdate"

    })


# ==========================
# HAPUS STOK
# ==========================
@stok_bp.route("/api/stok/<id>", methods=["DELETE"])
def hapus_stok(id):

    mongo.db.stok.delete_one({

        "_id": ObjectId(id)

    })

    return jsonify({

        "success": True,

        "message": "Data berhasil dihapus"

    })