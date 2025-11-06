# Image officielle Python
FROM python:3.11-slim

# Installer les dépendances
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY app.py .

# Port utilisé par Cloud Run
ENV PORT=8080
EXPOSE 8080

# Lancer l'application
CMD ["python", "app.py"]
