import joblib
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

# ===========================
# LOAD DATASET
# ===========================

df = pd.read_csv("ml/dataset_penjualan.csv")

print("========== DATASET ==========")
print(df)

# ===========================
# FEATURE ENGINEERING
# ===========================

df["tanggal"] = pd.to_datetime(df["tanggal"])

df["hari"] = df["tanggal"].dt.day
df["bulan"] = df["tanggal"].dt.month
df["tahun"] = df["tanggal"].dt.year

# ===========================
# X dan Y
# ===========================

X = df[
    [
        "hari",
        "bulan",
        "tahun",
        "total_order",
        "total_produk",
    ]
]

y = df["total_penjualan"]

# ===========================
# SPLIT DATA
# ===========================

if len(df) < 5:

    print("\n====================================")
    print("DATASET TERLALU SEDIKIT")
    print("Minimal 5 data untuk training")
    print("====================================")
    exit()

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
)

# ===========================
# TRAIN MODEL
# ===========================

model = LinearRegression()

model.fit(X_train, y_train)

# ===========================
# EVALUASI
# ===========================

prediksi = model.predict(X_test)

print("\n========== HASIL ==========")

print(
    "MAE :",
    mean_absolute_error(
        y_test,
        prediksi,
    ),
)

print(
    "RMSE :",
    mean_squared_error(
        y_test,
        prediksi,
        squared=False,
    ),
)

print(
    "R2 :",
    r2_score(
        y_test,
        prediksi,
    ),
)

# ===========================
# SIMPAN MODEL
# ===========================

joblib.dump(
    model,
    "ml/sales_model.pkl",
)

print("\nMODEL BERHASIL DISIMPAN")

print("Lokasi : ml/sales_model.pkl")