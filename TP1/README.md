# Compte rendu du TP1


## Etape 1 :

### Partie 1 : crée l'image
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

### Partie 2 : Publié l'image

ensuite sur azure il faut crée un Container registry
puis ajouter le compte des collegues pour qu'il puisse pousse des images dessus via les IAM
on active l'acces Administrateur via clé d'acces
Puis a la racines on execute les commandes ci dessous pour push sur le registre
```cmd
az login
az acr login --name infracloudynov
docker tag flask-api infracloudynov.azurecr.io/samples/flask-api:latest
docker push infracloudynov.azurecr.io/samples/flask-api:latest
```

Partie 3 : Does it work ?


```cmd
MacBook-Air-de-Remult:~ remult$ curl http://20.216.220.240:5000/hello
{"message":"Bonjour depuis l'API Flask !"}
```


## Etape 2 :
[api DOC](./API/api-doc.yaml)
