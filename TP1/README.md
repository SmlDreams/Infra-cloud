# Compte rendu du TP1


## Etape 1 :

Création de l'api Flask une api simple qui ecoute sur le port 5000
puis création d'un petit dockerfile pour lancer l'api partout

pour lancer l'API
Dans le dossier contenant Dockerfile
```cmd
docker build -t flask-api .
docker run -d -p 5000:5000 flask-api

# pour tester
curl http://localhost:5000/hello

```