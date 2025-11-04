# Étape 1 : Utiliser une image Python légère
FROM python:3.11-slim

# Étape 2 : Définir le dossier de travail
WORKDIR /app

# Étape 3 : Copier les fichiers nécessaires
COPY ./requirements.txt .

# Étape 4 : Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Étape 5 : Copier le code source
COPY . .

# Étape 6 : Exposer le port de l'application
EXPOSE 5000

# Étape 7 : Créer un utilisateur non-root (meilleure sécurité)
RUN useradd -m flaskuser
USER flaskuser

# Étape 8 : Définir le point d’entrée (serveur de prod)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
