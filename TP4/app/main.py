import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Lecture des variables d'environnement
APP_MESSAGE = os.environ.get("APP_MESSAGE", "Hello World")
UPLOAD_ALLOWED_EXT = os.environ.get("UPLOAD_ALLOWED_EXT", ".txt").split(",")
UPLOAD_PASSWORD = os.environ.get("UPLOAD_PASSWORD", "changeme")

UPLOAD_FOLDER = "/data"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Route GET /
@app.route("/", methods=["GET"])
def list_files():
    files = os.listdir(UPLOAD_FOLDER)
    return jsonify({"app_message": APP_MESSAGE, "files": files})

# Route POST /upload
@app.route("/upload", methods=["POST"])
def upload_file():
    password = request.form.get("password")
    file = request.files.get("file")

    if not file or not password:
        return jsonify({"error": "Missing file or password"}), 400

    if password != UPLOAD_PASSWORD:
        return jsonify({"error": "Invalid password"}), 403

    filename = secure_filename(file.filename)
    if not any(filename.endswith(ext) for ext in UPLOAD_ALLOWED_EXT):
        return jsonify({"error": "Invalid file extension"}), 400

    file.save(os.path.join(UPLOAD_FOLDER, filename))
    return jsonify({"message": f"File {filename} uploaded successfully"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
