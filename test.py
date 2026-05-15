from pymongo import MongoClient

print("Mulai koneksi...")

uri = "mongodb+srv://konveksi-user:admin123@cluster0.06x3naq.mongodb.net/konveksi_db?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri)

print("Client dibuat")

client.admin.command("ping")

print("MongoDB Connected!")