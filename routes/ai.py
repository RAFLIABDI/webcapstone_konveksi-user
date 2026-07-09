from flask import Blueprint, jsonify
from models.database import mongo
from collections import defaultdict
from datetime import datetime, timedelta

ai_bp = Blueprint("ai", __name__)


@ai_bp.route("/api/ai/dashboard", methods=["GET"])
def ai_dashboard():

    orders = list(mongo.db.orders.find())

    # =====================================
    # SUMMARY
    # =====================================

    total_penjualan = 0
    total_order = len(orders)
    total_produk = 0

    produk_counter = defaultdict(int)
    sales_counter = defaultdict(int)

    today = datetime.now()
    minggu_ini = today - timedelta(days=7)
    minggu_lalu = today - timedelta(days=14)

    total_minggu_ini = 0
    total_minggu_lalu = 0

    for order in orders:

        harga = int(order.get("harga", 0))
        jumlah = int(order.get("jumlah", 0))
        produk = order.get("produk", "-")

        total_penjualan += harga
        total_produk += jumlah

        produk_counter[produk] += jumlah

        created = order.get("created_at")

        if created:

            if isinstance(created, str):

                try:
                    created = datetime.fromisoformat(
                        created.replace("Z", "")
                    )
                except:
                    continue

            # Grafik penjualan
            tanggal = created.strftime("%d/%m")
            sales_counter[tanggal] += harga

            # Trend
            if created >= minggu_ini:
                total_minggu_ini += harga

            elif created >= minggu_lalu:
                total_minggu_lalu += harga

    rata_order = (
        total_penjualan // total_order
        if total_order > 0 else 0
    )

    # =====================================
    # PRODUK TERLARIS
    # =====================================

    produk_terlaris = "-"

    if produk_counter:
        produk_terlaris = max(
            produk_counter,
            key=produk_counter.get
        )

    # =====================================
    # TOP 5 PRODUCT
    # =====================================

    top_products = []

    sorted_produk = sorted(
        produk_counter.items(),
        key=lambda x: x[1],
        reverse=True
    )

    for nama, qty in sorted_produk[:5]:

        top_products.append({
            "produk": nama,
            "jumlah": qty
        })

    # =====================================
    # SALES HISTORY
    # =====================================

    sales_history = []

    for tanggal, total in sorted(sales_counter.items()):

        sales_history.append({
            "tanggal": tanggal,
            "penjualan": total
        })

    # =====================================
    # TREND
    # =====================================

    trend = "Stabil"
    persentase = 0

    if total_minggu_lalu > 0:

        persentase = round(
            (
                (total_minggu_ini - total_minggu_lalu)
                / total_minggu_lalu
            ) * 100,
            1
        )

        if persentase > 0:
            trend = "Naik"

        elif persentase < 0:
            trend = "Turun"

    # =====================================
    # FORECAST
    # =====================================

    forecast = round(
        total_minggu_ini * 1.10
    )

    # =====================================
    # AI SCORE
    # =====================================

    score = 50

    if trend == "Naik":
        score += 15

    if total_order >= 20:
        score += 10

    if total_produk >= 500:
        score += 10

    if forecast > total_minggu_ini:
        score += 10

    if produk_terlaris != "-":
        score += 5

    score = min(score, 100)

    # =====================================
    # INSIGHT AI
    # =====================================

    insight = []

    insight.append(
        f"Produk paling diminati adalah {produk_terlaris}."
    )

    insight.append(
        f"Total penjualan mencapai Rp {total_penjualan:,}."
    )

    if trend == "Naik":

        insight.append(
            f"Penjualan meningkat {persentase}% dibanding minggu sebelumnya."
        )

    elif trend == "Turun":

        insight.append(
            f"Penjualan turun {abs(persentase)}% dibanding minggu sebelumnya."
        )

    else:

        insight.append(
            "Penjualan relatif stabil."
        )

    insight.append(
        f"Prediksi penjualan minggu depan sekitar Rp {forecast:,}."
    )

    insight.append(
        f"Disarankan menambah stok {produk_terlaris}."
    )

    # =====================================
    # RETURN JSON
    # =====================================

    return jsonify({

        "success": True,

        "data": {

            "summary": {

                "total_penjualan": total_penjualan,
                "total_order": total_order,
                "total_produk": total_produk,
                "produk_terlaris": produk_terlaris,
                "rata_order": rata_order

            },

            "top_products": top_products,

            "sales_history": sales_history,

            "trend": {

                "status": trend,
                "persentase": persentase

            },

            "forecast": {

                "minggu_depan": forecast

            },

            "ai_score": score,

            "insight": insight

        }

    })