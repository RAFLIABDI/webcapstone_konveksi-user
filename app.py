import os
from flask import Flask

# Config
from config import Config
from extensions import mail

# auth
from routes.auth import auth_bp

# Database
from models.database import mongo

# Blueprint
from routes.home import home_bp
from routes.order import order_bp
from routes.tracking import tracking_bp

# upload desain
from flask import send_from_directory

app = Flask(__name__)

app.config.from_object(Config)

mail.init_app(app)

app.config["UPLOAD_FOLDER"] = "uploads"

# MongoDB Config
app.config["MONGO_URI"] = Config.MONGO_URI

# Init MongoDB
mongo.init_app(app)

# Register Blueprint
app.register_blueprint(home_bp)
app.register_blueprint(order_bp)
app.register_blueprint(tracking_bp)
app.register_blueprint(auth_bp)

@app.route("/test-db")
def test_db():

    mongo.db.orders.insert_one({
        "nama_customer": "Rafli",
        "produk": "Kaos Sablon",
        "status": "pending"
    })

    return "Data berhasil disimpan!"

@app.route("/uploads/<path:filename>")
def uploaded_file(filename):

    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )

# Run App
if __name__ == "__main__":

    app.run(

        debug=True,

        host="0.0.0.0",

        port=5000

    )