# Compte rendu TP4 Partie 1


## 1. Préparation du cloud

```cmd
gcloud projects create lorens060104 --name="TP4-InfraCloud"
```

## 2. Cluster Kubernetes

Créer un cluster managé :
2 nœuds minimum.
Version Kubernetes récente par défaut.Module 10  Kubernetes managé  AKS / EKS / GKE7

```gcc
gcloud container clusters create tp4-kubcluster \
  --zone=europe-west1-b \
  --machine-type=e2-medium \
  --num-nodes=2 \
  --max-nodes=3 \
  --project=lorens060104
```

Récupérer la configuration kubeconfig .
```gcc
gcloud container clusters get-credentials tp4-kubcluster \
  --zone=europe-west1-b \
  --project=lorens060104
```
Vérifier lʼaccès avec kubectl get nodes .

```cmd
kubectl get nodes
NAME                                            STATUS   ROLES    AGE    VERSION
gke-tp4-kubcluster-default-pool-bd6b36df-csg9   Ready    <none>   105s   v1.33.5-gke.1201000
gke-tp4-kubcluster-default-pool-bd6b36df-tvh1   Ready    <none>   106s   v1.33.5-gke.1201000
```

## 3. Namespace et objets de configuration
Créer un namespace tp-app .
Créer un ConfigMap dans tp-app avec au minimum :
APP_MESSAGE (string libre).
UPLOAD_ALLOWED_EXT (ex : .txt ).
Créer un Secret dans tp-app avec :
UPLOAD_PASSWORD (mot de passe attendu pour lʼupload).

j'ai tous fait via des commandes et pas des fichier yaml car plus simple pour le rendu

```cmd
kubectl create namespace tp-app
kubectl create configmap app-config \
  --namespace=tp-app \
  --from-literal=APP_MESSAGE="Hello from Kubernetes!" \
  --from-literal=UPLOAD_ALLOWED_EXT=".txt"
kubectl create secret generic app-secret \
  --namespace=tp-app \
  --from-literal=UPLOAD_PASSWORD="MonSuperMotDePasse123"
```

## 4. Application Python

[APP](./app/)



## 5. Conteneurisation et registry
Créer un Dockerfile :
image de base Python officielle,
copie de requirements.txt ,
installation des dépendances,
copie de main.py ,
exposition du port de lʼapp (ex  8000,
commande de démarrage de lʼapp.
Builder lʼimage Docker en local.
Tagger lʼimage pour le registry du cloud :
GCP  Artifact Registry,
Pousser lʼimage dans le registry choisi.

``cmd
# Crée un dépôt docker dans Artifact Registry
gcloud artifacts repositories create tp-app-repo \
  --repository-format=docker \
  --location=europe-west1
```

## 6. Stockage – PVC RWX
 Créer dans le namespace tp-app un PVC nommé shared-pvc avec :
mode dʼaccès : ReadWriteMany ,
taille  1Gi,
 Vérifier que le PVC passe en état Bound


## 7. Déploiement de lʼapplication
 Créer un Deployment dans le namespace tp-app avec :Module 10  Kubernetes managé  AKS / EKS / GKE9
2 replicas,
container utilisant lʼimage poussée au registry,
envFrom ou env pour :
injecter le ConfigMap APP_MESSAGE, UPLOAD_ALLOWED_EXT,
injecter le Secret UPLOAD_PASSWORD,
volume :
type : persistentVolumeClaim ,
claimName: shared-pvc ,
volumeMounts :
monter le volume sur /data .
 Appliquer le manifeste du Deployment.
 Vérifier que les Pods passent en Running .


## 8. Exposition de lʼapplication
 Créer un Service de type LoadBalancer dans tp-app :
cible : les Pods du Deployment,
port externe  80,
port cible : port de lʼapp dans le container (ex  8000.
 Appliquer le Service.
 Récupérer lʼIP publique du Service.

## 9. Tests fonctionnels
 Appeler GET / sur lʼIP publique :
vérifier que la liste des fichiers est vide au départ.
 Tester POST /upload :
avec un mauvais password → upload refusé,
avec le bon password (valeur du Secret) et une extension autorisée →
upload accepté.Module 10  Kubernetes managé  AKS / EKS / GKE10
 Refaire GET / :
vérifier que le fichier apparaît dans la liste

## 10. Tests RWX et stateless
 Vérifier que les 2 Pods du Deployment sont en Running .
 Se connecter en shell sur le premier Pod :
lister les fichiers dans /data .
 Se connecter sur le deuxième Pod :
vérifier que les mêmes fichiers sont visibles dans /data .
 Supprimer un des Pods du Deployment.
 Vérifier :
le Service continue de répondre via lʼautre Pod,
le Pod recréé par le Deployment voit immédiatement les fichiers dans
/data 

## 11. Nettoyage
Dans le namespace tp-app , supprimer :
Deployment,
Service,
PVC,
ConfigMap,
Secret,
namespace tp-app .


Dans le cloud, supprimer :
le cluster Kubernetes managé,
le registry utilisé,
les ressources associées créées uniquement pour le TP Resource
Group, projet, etc.).