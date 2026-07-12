from flask import Blueprint, render_template
from models.database import mongo

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def home():

    # =====================================
    # Data terbaru (opsional)
    # =====================================
    berita = list(
        mongo.db.news_fashion_trends.find()
        .sort("_id", -1)
        .limit(10)
    )

    # =====================================
    # Data grafik
    # =====================================
    pipeline = [

        {
            "$match": {
                "keyword_used": {
                    "$nin": [None, "", "Lainnya"]
                }
            }
        },

        {
            "$group": {
                "_id": "$keyword_used",
                "jumlah": {
                    "$sum": 1
                }
            }
        },

        {
            "$sort": {
                "jumlah": -1
            }
        }

    ]

    hasil = list(
        mongo.db.news_fashion_trends.aggregate(pipeline)
    )

    labels = []
    values = []

    for item in hasil:
        labels.append(item["_id"])
        values.append(item["jumlah"])

    # =====================================
    # Statistik Dashboard
    # =====================================

    total_video = mongo.db.news_fashion_trends.count_documents({})

    kaos = mongo.db.news_fashion_trends.count_documents({
        "keyword_used": "kaos"
    })

    totebag = mongo.db.news_fashion_trends.count_documents({
        "keyword_used": "totebag"
    })

    polo = mongo.db.news_fashion_trends.count_documents({
        "keyword_used": "polo"
    })

    lanyard = mongo.db.news_fashion_trends.count_documents({
        "keyword_used": "lanyard"
    })

    idcard = mongo.db.news_fashion_trends.count_documents({
        "keyword_used": "id card"
    })

    # =====================================
    # Update Terakhir
    # =====================================

    data_terbaru = mongo.db.news_fashion_trends.find_one(
        sort=[("scraped_at", -1)]
    )

    last_update = None

    if data_terbaru:
        last_update = data_terbaru.get("scraped_at")

    # =====================================
    # Render
    # =====================================

    return render_template(

        "index.html",

        berita=berita,

        labels=labels,

        values=values,

        total_video=total_video,

        kaos=kaos,

        totebag=totebag,

        polo=polo,

        lanyard=lanyard,

        idcard=idcard,

        last_update=last_update

    )


@home_bp.route("/produk")
def produk():
    return render_template("produk.html")


@home_bp.route("/cek-data")
def cek_data():

    data = list(
        mongo.db.news_fashion_trends.find().limit(5)
    )

    hasil = []

    for d in data:

        hasil.append({

            "title": d.get("title"),

            "keyword_used": d.get("keyword_used"),

            "source": d.get("source")

        })

    return hasil