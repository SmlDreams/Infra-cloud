from flask import Flask, jsonify

# Création de l'application Flask
app = Flask(__name__)

# Route REST simple
@app.route('/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Bonjour depuis l'API Flask !"}), 200

# Point d'entrée principal
if __name__ == '__main__':
    # Lancer sur toutes les interfaces, port 8080 (par défaut)
    app.run(host='0.0.0.0', port=8080, debug=True)
