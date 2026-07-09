from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import jsonify

from werkzeug.utils import secure_filename

from datetime import datetime
from datetime import timedelta

from rembg import remove
from PIL import Image

from bson import ObjectId

from flask_mail import Message

from extensions import mail

import random
import os

# Database
from models.database import mongo

order_bp = Blueprint(
    'order',
    __name__
)

# Upload Folder
UPLOAD_FOLDER = "static/uploads"

# Allowed File
ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "pdf"
}

# =========================
# VALIDASI FILE
# =========================
def allowed_file(filename):

    return "." in filename and \
           filename.rsplit(
               ".", 1
           )[1].lower() in ALLOWED_EXTENSIONS

# =========================
# GENERATE OTP
# =========================
def generate_otp():

    return str(

        random.randint(
            100000,
            999999
        )

    )

# =========================
# ACTIVITY LOG
# =========================
def save_log(activity, ip):

    mongo.db.logs.insert_one({

        "activity": activity,

        "ip_address": ip,

        "created_at": datetime.now()

    })

# =========================
# GENERATE ORDER CODE
# =========================
def generate_order_code():

    total_order = (
        mongo.db.orders
        .count_documents({})
    ) + 1

    tahun = datetime.now().year

    return f"ORD{tahun}{total_order:03d}"

# =========================
# ORDER
# =========================
@order_bp.route(
    "/order",
    methods=["GET", "POST"]
)
def order():

    produk_pilihan = request.args.get(
        "produk"
    )

    if request.method == "POST":

        # =========================
        # FORM DATA
        # =========================

        nama = request.form.get(
            "nama"
        )

        email = request.form.get(
            "email"
        ) or ""

        whatsapp = request.form.get(
            "whatsapp"
        )

        produk = request.form.get(
            "produk"
        )

        catatan = request.form.get(
            "catatan"
        )

        harga = int(
            request.form.get(
                "harga"
            ) or 0
        )

        jumlah = 0
        variasi = []

        # =========================
        # PRODUK APPAREL
        # =========================

        if (

            produk == "Kaos Sablon"

            or

            produk == "Polo Bordir"

        ):

            s_pendek = int(
                request.form.get(
                    "s_pendek"
                ) or 0
            )

            s_panjang = int(
                request.form.get(
                    "s_panjang"
                ) or 0
            )

            m_pendek = int(
                request.form.get(
                    "m_pendek"
                ) or 0
            )

            m_panjang = int(
                request.form.get(
                    "m_panjang"
                ) or 0
            )

            l_pendek = int(
                request.form.get(
                    "l_pendek"
                ) or 0
            )

            l_panjang = int(
                request.form.get(
                    "l_panjang"
                ) or 0
            )

            xl_pendek = int(
                request.form.get(
                    "xl_pendek"
                ) or 0
            )

            xl_panjang = int(
                request.form.get(
                    "xl_panjang"
                ) or 0
            )

            jumlah = (

                s_pendek +

                s_panjang +

                m_pendek +

                m_panjang +

                l_pendek +

                l_panjang +

                xl_pendek +

                xl_panjang

            )

            variasi = [

                {
                    "size": "S",
                    "jenis": "Pendek",
                    "qty": s_pendek
                },

                {
                    "size": "S",
                    "jenis": "Panjang",
                    "qty": s_panjang
                },

                {
                    "size": "M",
                    "jenis": "Pendek",
                    "qty": m_pendek
                },

                {
                    "size": "M",
                    "jenis": "Panjang",
                    "qty": m_panjang
                },

                {
                    "size": "L",
                    "jenis": "Pendek",
                    "qty": l_pendek
                },

                {
                    "size": "L",
                    "jenis": "Panjang",
                    "qty": l_panjang
                },

                {
                    "size": "XL",
                    "jenis": "Pendek",
                    "qty": xl_pendek
                },

                {
                    "size": "XL",
                    "jenis": "Panjang",
                    "qty": xl_panjang
                }

            ]

        else:

            jumlah = int(
                request.form.get(
                    "simpleQty"
                ) or 0
            )

        # =========================
        # UPLOAD FILE
        # =========================

        file = request.files.get(
            "desain"
        )

        nama_file = None

        if file and file.filename != "":

            if allowed_file(file.filename):

                nama_file = secure_filename(
                    file.filename
                )

                file_path = os.path.join(

                    UPLOAD_FOLDER,

                    nama_file

                )

                # SAVE ORIGINAL
                file.save(file_path)

                # =========================
                # REMOVE BACKGROUND
                # =========================

                if (

                    produk == "Kaos Sablon"

                    or

                    produk == "Polo Bordir"

                ):

                    try:

                        input_image = Image.open(
                            file_path
                        )

                        output_image = remove(
                            input_image
                        )

                        removed_filename = (

                            "removed_"

                            +

                            nama_file.rsplit(
                                ".", 1
                            )[0]

                            +

                            ".png"

                        )

                        removed_path = os.path.join(

                            "static/removed",

                            removed_filename

                        )

                        output_image.save(
                            removed_path
                        )

                        nama_file = removed_filename

                    except Exception as e:

                        print(

                            "Remove background error:",

                            e

                        )

        # =========================
        # ORDER CODE
        # =========================

        kode_order = generate_order_code()

        # =========================
        # OTP
        # =========================

        otp = generate_otp()

        otp_expired = (

            datetime.now()

            +

            timedelta(minutes=5)

        )

        # =========================
        # SAVE ORDER
        # =========================

        mongo.db.orders.insert_one({

            "kode_order": kode_order,

            "nama_customer": nama,

            "email": email,

            "whatsapp": whatsapp,

            "produk": produk,

            "jumlah": jumlah,

            "variasi": variasi,

            "catatan": catatan,

            "file_desain": nama_file,

            "harga": harga,

            "status": "pending",

            "otp": otp,

            "otp_expired": otp_expired,

            "is_verified": False,

            "created_at": datetime.now()

        })

        # =========================
        # SEND OTP EMAIL
        # =========================

        if not email:

            return "Email wajib diisi"

        msg = Message(

            "OTP Verifikasi Order",

            sender="EMAIL_GMAIL_KAMU",

            recipients=[email]

        )

        msg.body = f"""

Kode OTP anda:

{otp}

OTP berlaku selama 5 menit.

"""

        mail.send(msg)

        # =========================
        # SAVE LOG
        # =========================

        save_log(

            f"Order baru: {kode_order}",

            request.remote_addr

        )

        # =========================
        # REDIRECT OTP
        # =========================

        return redirect(

            url_for(

                "order.verify_page",

                kode_order=kode_order

            )

        )

    return render_template(

        "order.html",

        produk_pilihan=produk_pilihan

    )

# =========================
# HALAMAN OTP
# =========================
@order_bp.route(
    "/verify/<kode_order>"
)
def verify_page(kode_order):

    return render_template(

        "verify_otp.html",

        kode_order=kode_order

    )

# =========================
# VERIFY OTP
# =========================
@order_bp.route(
    "/verify-otp",
    methods=["POST"]
)
def verify_otp():

    kode_order = request.form.get(
        "kode_order"
    )

    otp_input = request.form.get(
        "otp"
    )

    order = mongo.db.orders.find_one({

        "kode_order": kode_order

    })

    # ORDER TIDAK ADA
    if not order:

        return "Order tidak ditemukan"

    # OTP EXPIRED
    if datetime.now() > order[
        "otp_expired"
    ]:

        return "OTP expired"

    # OTP SALAH
    if otp_input != order[
        "otp"
    ]:

        return "OTP salah"

    # VERIFIED
    mongo.db.orders.update_one(

        {
            "kode_order": kode_order
        },

        {
            "$set": {

                "is_verified": True

            }
        }

    )

    # SAVE LOG
    save_log(

        f"OTP verified: {kode_order}",

        request.remote_addr

    )

    return redirect(

        url_for(

            "order.sukses",

            kode_order=kode_order

        )

    )

# =========================
# API ORDERS
# =========================
@order_bp.route(
    "/api/orders",
    methods=["GET"]
)
def api_orders():

    orders = mongo.db.orders.find({

        "is_verified": True

    }).sort(

        "created_at",

        -1

    )

    data = []

    for order in orders:

        data.append({

            "id": str(
                order["_id"]
            ),

            "kode_order":
                order.get(
                    "kode_order"
                ),

            "nama_customer":
                order.get(
                    "nama_customer"
                ),

            "produk":
                order.get(
                    "produk"
                ),

            "jumlah":
                order.get(
                    "jumlah"
                ),

            "status":
                order.get(
                    "status"
                ),
            
            "variasi":
                order.get(
                    "variasi",
                    []
                ),
            
            "catatan":
                order.get(
                    "catatan",
                    ""
                ),

            "file_desain":
                order.get(
                    "file_desain"
                ),
            
            "harga":
            order.get(
                "harga",
                0
            ),

            "created_at": str(

                order.get(
                    "created_at"
                )

            )

        })

    return jsonify({

        "success": True,

        "data": data

    })

# =========================
# DASHBOARD MONITOR
# =========================
@order_bp.route(
    "/api/dashboard",
    methods=["GET"]
)
def dashboard():

    total_order = (
        mongo.db.orders
        .count_documents({

            "is_verified": True

        })
    )

    pending = (
        mongo.db.orders
        .count_documents({

            "status": "pending",

            "is_verified": True

        })
    )

    sewing = (
        mongo.db.orders
        .count_documents({

            "status": "SEWING",

            "is_verified": True

        })
    )

    printing = (
        mongo.db.orders
        .count_documents({

            "status": "PRINTING",

            "is_verified": True

        })
    )

    done = (
        mongo.db.orders
        .count_documents({

            "status": "DONE",

            "is_verified": True

        })
    )

    return jsonify({

        "success": True,

        "data": {

            "total_order":
                total_order,

            "pending":
                pending,

            "sewing":
                sewing,

            "printing":
                printing,

            "done":
                done

        }

    })

# =========================
# UPDATE STATUS
# =========================
@order_bp.route(
    "/api/update-status/<id>",
    methods=["PUT"]
)
def update_status(id):

    data = request.json

    status = data.get(
        "status"
    )

    mongo.db.orders.update_one(

        {
            "_id": ObjectId(id)
        },

        {
            "$set": {

                "status": status

            }

        }

    )

    # SAVE LOG
    save_log(

        f"Update status: {status}",

        request.remote_addr

    )

    return jsonify({

        "success": True,

        "message":
            "Status berhasil diupdate"

    })


# =========================
# DELETE ORDER
# =========================
@order_bp.route(
    "/api/orders/<id>",
    methods=["DELETE"]
)
def delete_order(id):

    result = mongo.db.orders.delete_one({

        "_id": ObjectId(id)

    })

    if result.deleted_count == 0:

        return jsonify({

            "success": False,

            "message": "Order tidak ditemukan"

        }),404

    save_log(

        f"Hapus order {id}",

        request.remote_addr

    )

    return jsonify({

        "success": True,

        "message": "Order berhasil dihapus"

    })


# =========================
# SUCCESS
# =========================
@order_bp.route(
    "/sukses"
)
def sukses():

    kode_order = request.args.get(
        "kode_order"
    )

    return render_template(

        "sukses.html",

        kode_order=kode_order

    )