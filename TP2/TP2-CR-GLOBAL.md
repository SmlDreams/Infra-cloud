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

### Partie 3 : Does it work ?


```cmd
MacBook-Air-de-Remult:~ remult$ curl http://20.216.220.240:5000/hello
{"message":"Bonjour depuis l'API Flask !"}
```


## Etape 2 :

### Partie 1 :

[api DOC](./API/api-doc.yaml)

### Partie 2 :

on crée l'api mgmt puis on crée une nouvelle api et dans design on ajoute le yaml de la section précedente on peut mtn faire un test et ca marche

```cmd
HTTP response

HTTP/1.1 200 OK
content-length: 43
content-type: application/json
date: Tue, 04 Nov 2025 11:06:11 GMT
vary: Origin
    
{
    "message": "Bonjour depuis l'API Flask !"
}
```

### Partie 3 :

exposé l'api via le mgmt ne pas oublier de decoché required subscription ...

```cmd
MacBook-Air-de-Remult:~ remult$ curl http://api-test-mgmt.azure-api.net/hello
{"message":"Bonjour depuis l'API Flask !"}
```

## Etape 3 :

[le code source est dispo ici](./WEB/)

### Partie 1 :

on crée le static website et on link azure a github pour qu'il puissent Download les bon fichier de se repo 
ou alors on suit le tp et fait un storage account
crée une class container web

### partie 2 : 
liaison via github
ou si on suit le tp on televerse les deux fichier dans le container

### Partie 3 :

on enable le site static via le storage account

#### Partie 4 : Does It work?

les deux request curl l'api et le site sont bien accesible
```cmd
MacBook-Air-de-Remult:tftp remult$ curl https://websitestorageinfracloud.z28.web.core.windows.net/
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Sasuke Dark API</title>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap">
</head>
<body>
    <h1>Sasuke Dark API Call</h1>
    <p>Appuie sur le bouton pour appeler l'API :</p>
    <button id="callApi">Appeler l'API</button>
    <div id="response"></div>

    <script src="script.js"></script>
</body>
</html>
MacBook-Air-de-Remult:tftp remult$ curl http://api-test-mgmt.azure-api.net/hello
{"message":"Bonjour depuis l'API Flask !"}
```

## Etape 4 :

Cette partie est ecrite en bricolant avec la doc et des tuto car l'offre n'est pas dispo dans notre pack student


### Partie 1 :

on crée le azure front door ....
on ajoute notre storage account comme origine via backend pool
on laisse les option pour la publication par default 



### Partie 2 :


ensuite on creé le front end on laisse le domain fournit par azure

on active https avec un certificats géré par azure.


### Partie 3 :

on crée un deuxieme backend pool pour l'api
sur le front on crée une nouvelle route avec en endpoint le meme domain mais avec pattern de base /api
donc /api/hello pour acceder a l'api


on ajoute la nouvelle route aussi dans l'api mgmt
