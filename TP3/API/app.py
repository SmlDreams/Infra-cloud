from flask import Flask, jsonify
from google.cloud import storage
import os

app = Flask(__name__)

# Nom du bucket via variable d'environnement
BUCKET_NAME = os.environ.get("BUCKET_NAME")

# Client Cloud Storage
client = storage.Client()
bucket = client.bucket(BUCKET_NAME)

@app.route("/list")
def list_objects():
    """Liste les objets du bucket et retourne un JSON."""
    try:
        blobs = bucket.list_blobs()
        files = [blob.name for blob in blobs]
        return jsonify(files)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Expose l'application sur le port défini par Cloud Run
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)