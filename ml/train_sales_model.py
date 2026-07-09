import os
import sys

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from pymongo import MongoClient
from config import Config
import pandas as pd

# ===========================
# CONNECT DATABASE
# ===========================

client = MongoClient(Config.MONGO_URI)
db = client.get_default_database()

orders = list(db.orders.find())

df = pd.DataFrame(orders)

# ===========================
# PREPROCESSING
# ===========================

df = df[
    [
        "created_at",
        "jumlah",
        "harga",
        "produk"
    ]
]

df = df.dropna()

df["jumlah"] = df["jumlah"].astype(int)
df["harga"] = df["harga"].astype(float)
df["created_at"] = pd.to_datetime(df["created_at"])

# ===========================
# AGREGASI PER HARI
# ===========================

daily_sales = (
    df.groupby(df["created_at"].dt.date)
    .agg(
        total_order=("jumlah", "count"),
        total_produk=("jumlah", "sum"),
        total_penjualan=("harga", "sum")
    )
    .reset_index()
)

daily_sales.rename(
    columns={
        "created_at": "tanggal"
    },
    inplace=True
)

# ===========================
# SIMPAN CSV
# ===========================

os.makedirs("ml", exist_ok=True)

daily_sales.to_csv(
    "ml/dataset_penjualan.csv",
    index=False
)

print("\n==============================")
print("DATASET BERHASIL DIBUAT")
print("==============================")

print(daily_sales)

print("\nTotal Hari :", len(daily_sales))

print("\nFile : ml/dataset_penjualan.csv")