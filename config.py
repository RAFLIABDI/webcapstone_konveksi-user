import os

from dotenv import load_dotenv

load_dotenv()

class Config:

    # =========================
    # MONGODB
    # =========================
    MONGO_URI = os.getenv(
        "MONGO_URI"
    )

    # =========================
    # FLASK MAIL
    # =========================
    MAIL_SERVER = "smtp.gmail.com"

    MAIL_PORT = 587

    MAIL_USE_TLS = True

    MAIL_USERNAME = "raflinurikhwanabdi@gmail.com"

    MAIL_PASSWORD = "pnje idra ollp pqcd"