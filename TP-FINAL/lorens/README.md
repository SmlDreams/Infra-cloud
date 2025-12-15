## Partie 0 : setup du projet

```sh
# création du projet
gcloud projects create tpfinal-lorens --name="TP-FINAL"
gcloud config set project tpfinal-lorens
# la facturation
gcloud billing projects link tpfinal-lorens   --billing-account=011051-XXXXX-XXXXX
```

## Partie 1 : Création de l'image pour docker

```sh
docker build -f deployments/pre-prod/Dockerfile .
docker images
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
<none>       <none>    8a10fb514480   46 seconds ago   696MB
docker tag 8a10fb514480 europe-west1-docker.pkg.dev/tpfinal-lorens/vaultaire/vaultaire-core:latest
```

## Partie 2 : Création du registre docker  

```sh
# création du registre sur le cloud
gcloud artifacts repositories create vaultaire   --repository-format=docker   --location=europe-west1   --description="Vaultaire Docker Registry"
# push push
docker push europe-west1-docker.pkg.dev/tpfinal-lorens/vaultaire/vaultaire-core:latest
gcloud artifacts docker images list europe-west1-docker.pkg.dev/tpfinal-lorens/vaultaire
Listing items under project tpfinal-lorens, location europe-west1, repository vaultaire.

IMAGE                                                                DIGEST                                                                   CREATE_TIME          UPDATE_TIME          SIZE
europe-west1-docker.pkg.dev/tpfinal-lorens/vaultaire/vaultaire-core  sha256:8b0a6a272a4ddc4b36d5a2819007f4b0f54c1b153794ba47a6330d5e192d2389  2025-12-15T10:57:16  2025-12-15T10:57:16  175769688
```

## Partie 3 : Création du cluster Kubernetes

```sh
gcloud container clusters create tpfinal-kubcluster \
  --zone=europe-west1-b \
  --machine-type=e2-medium \
  --num-nodes=2 \
  --max-nodes=3 \
  --project=tpfinal-lorens

gcloud container clusters get-credentials tpfinal-kubcluster \
  --zone=europe-west1-b \
  --project=tpfinal-lorens
```

## Partie 4 : Déploiement de l'app

```sh
gcloud auth print-access-token | kubectl create secret docker-registry vaultaire-registry-secret     --docker-server=europe-west1-docker.pkg.dev     --docker-username=oauth2accesstoken     --docker-password="$(gcloud auth print-access-token)"     --docker-email=ton_email@gmail.com

kubectl create configmap vaultaire-config     --from-file=vaultaire.conf=config/server_conf.yaml 

kubectl apply -f ./k8S/vaultaire-db.yaml
kubectl apply -f ./k8S/vaultaire-ad.yaml

kubectl get pods
NAME                            READY   STATUS    RESTARTS   AGE
vaultaire-ad-5678ffc5db-pv2j2   1/1     Running   0          2m50s
vaultaire-db-5fc6cb4fb7-dzhxk   1/1     Running   0          12m
```

## Partie 5 : Dédiée au cluster kub


cluster gère uniquement par le compte de service dédié
```sh
gcloud iam service-accounts create vaultaire-gke \
  --display-name "Vaultaire GKE Service Account"
gcloud projects add-iam-policy-binding tpfinal-lorens \
  --member="serviceAccount:vaultaire-gke@tpfinal-lorens.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.reader"
gcloud projects add-iam-policy-binding tpfinal-lorens \
  --member="serviceAccount:vaultaire-gke@tpfinal-lorens.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.reader"
gcloud container clusters create tpfinal-kubcluster \
  --zone=europe-west1-b \
  --machine-type=e2-medium \
  --num-nodes=2 \
  --service-account=vaultaire-gke@tpfinal-lorens.iam.gserviceaccount.com \
  --scopes=https://www.googleapis.com/auth/cloud-platform
```

## partie 6 : CI

pas mise en place mais fonctionelle il manque la liaison via un compte avec les bonnes permission
[ici](/.github/workflows/lorens.yaml)