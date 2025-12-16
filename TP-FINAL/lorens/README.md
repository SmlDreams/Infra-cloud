# Compte Rendu du TP Final - Déploiement de Vaultaire sur GCP


### Rappel des TPs Précédents Intégrés

- **TP2** : Introduction à la conteneurisation avec Docker, publication d'images sur Azure Container Registry, exposition d'APIs via API Management, et déploiement de sites statiques.
- **TP3** : Gestion des identités et accès (IAM) sur GCP, création de comptes de service, rôles et permissions, ainsi que la délégation via l'impersonation.
- **TP4** : Orchestration avec Kubernetes, déploiement d'applications, sécurité opérationnelle (RBAC, Pod Security Standards), et introduction à CI/CD avec Helm et ArgoCD.

Le projet final combine ces éléments pour créer un environnement de production sécurisé et automatisé.

## Partie 0 : Setup du Projet GCP

### Création du Projet
En référence au TP3, nous créons un nouveau projet GCP dédié au TP final.

```sh
# Création du projet
gcloud projects create tpfinal-lorens --name="TP-FINAL"
gcloud config set project tpfinal-lorens

# Liaison à la facturation (nécessite un compte de facturation existant)
gcloud billing projects link tpfinal-lorens --billing-account=011051-XXXXX-XXXXX
```

Cette étape établit l'environnement de base, similaire à la création de projets dans TP3, en veillant à la séparation des ressources pour une meilleure gestion et sécurité.

## Partie 1 : Création de l'Image Docker pour Vaultaire

### Construction de l'Image
Inspiré du TP2 où nous avons conteneurisé une API Flask, nous construisons l'image Docker pour Vaultaire.

```sh
# Construction de l'image (le Dockerfile se trouve dans deployments/pre-prod/)
docker build -f deployments/pre-prod/Dockerfile .
docker images
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
<none>       <none>    8a10fb514480   46 seconds ago   696MB
```

L'image inclut l'application Vaultaire avec toutes ses dépendances, permettant un déploiement cohérent et reproductible.

## Partie 2 : Création du Registre Docker (Artifact Registry)

### Configuration du Registre
Suite au TP2 (Azure Container Registry) et TP3 (permissions GCP), nous créons un registre privé sur GCP.

```sh
# Création du registre sur GCP
gcloud artifacts repositories create vaultaire \
  --repository-format=docker \
  --location=europe-west1 \
  --description="Vaultaire Docker Registry"

# Tag et push de l'image
docker tag 8a10fb514480 europe-west1-docker.pkg.dev/tpfinal-lorens/vaultaire/vaultaire-core:latest
docker push europe-west1-docker.pkg.dev/tpfinal-lorens/vaultaire/vaultaire-core:latest

# Vérification
gcloud artifacts docker images list europe-west1-docker.pkg.dev/tpfinal-lorens/vaultaire
```

Cette étape sécurise le stockage des images et contrôle l'accès via IAM, comme vu dans TP3.

## Partie 3 : Création du Cluster Kubernetes

### Provisionnement du Cluster GKE
En s'appuyant sur TP4, nous déployons un cluster Kubernetes managé.

```sh
gcloud container clusters create tpfinal-kubcluster \
  --zone=europe-west1-b \
  --machine-type=e2-medium \
  --num-nodes=2 \
  --max-nodes=3 \
  --project=tpfinal-lorens

# Récupération des credentials
gcloud container clusters get-credentials tpfinal-kubcluster \
  --zone=europe-west1-b \
  --project=tpfinal-lorens
```

Le cluster fournit une plateforme d'orchestration scalable et résiliente pour nos services.

## Partie 4 : Déploiement de l'Application

### Configuration et Déploiement
Nous déployons les composants de Vaultaire sur Kubernetes, utilisant les concepts de TP4.

```sh
# Création du secret pour l'accès au registre
gcloud auth print-access-token | kubectl create secret docker-registry vaultaire-registry-secret \
  --docker-server=europe-west1-docker.pkg.dev \
  --docker-username=oauth2accesstoken \
  --docker-password="$(gcloud auth print-access-token)" \
  --docker-email=ton_email@gmail.com

# Création de la ConfigMap pour la configuration
kubectl create configmap vaultaire-config \
  --from-file=vaultaire.conf=config/server_conf.yaml

# Déploiement des services
kubectl apply -f ./k8S/vaultaire-db.yaml
kubectl apply -f ./k8S/vaultaire-ad.yaml

# Vérification
kubectl get pods
NAME                            READY   STATUS    RESTARTS   AGE
vaultaire-ad-5678ffc5db-pv2j2   1/1     Running   0          2m50s
vaultaire-db-5fc6cb4fb7-dzhxk   1/1     Running   0          12m
```

Cette phase applique les principes de déploiement Kubernetes vus en TP4, avec gestion des secrets et configurations.

## Partie 5 : Sécurité du Cluster avec Comptes de Service

### Configuration IAM pour le Cluster
Référence directe au TP3 sur les comptes de service et à TP4 sur la sécurité K8s.

```sh
# Création d'un compte de service dédié
gcloud iam service-accounts create vaultaire-gke \
  --display-name "Vaultaire GKE Service Account"

# Attribution des permissions nécessaires
gcloud projects add-iam-policy-binding tpfinal-lorens \
  --member="serviceAccount:vaultaire-gke@tpfinal-lorens.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.reader"

# Création du cluster avec ce compte de service
gcloud container clusters create tpfinal-kubcluster \
  --zone=europe-west1-b \
  --machine-type=e2-medium \
  --num-nodes=2 \
  --service-account=vaultaire-gke@tpfinal-lorens.iam.gserviceaccount.com \
  --scopes=https://www.googleapis.com/auth/cloud-platform
```

Cette approche limite les permissions du cluster, appliquant le principe du moindre privilège vu en TP3 et TP4.

## Partie 6 : Intégration CI/CD

### Pipeline GitHub Actions
Bien que partiellement fonctionnel, le pipeline CI/CD s'inspire des concepts de TP4.

Le workflow [lorens.yaml](/.github/workflows/lorens.yaml) automatise :
- L'authentification GCP
- La construction et le push de l'image Docker
- Le déploiement sur GKE

Cependant, il nécessite la configuration d'un secret `GCP_SA_KEY` contenant la clé JSON d'un compte de service avec les permissions appropriées (Artifact Registry et GKE).

### Améliorations Requises
- Créer un compte de service dédié pour CI/CD
- Générer et stocker la clé dans GitHub Secrets
- Ajouter des tests automatisés
- Implémenter des déploiements progressifs (blue-green ou canary)

## Partie 7 : Déploiement de la Base de Données MariaDB plus propre

### Configuration MariaDB sur Kubernetes

Pour la persistance des données de Vaultaire, nous déployons une instance MariaDB directement sur Kubernetes via des manifests YAML.

```yaml
# Extrait du fichier vaultaire-db.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: vaultaire-db-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vaultaire-db
spec:
  replicas: 1
  selector:
    matchLabels:
      app: vaultaire-db
  template:
    metadata:
      labels:
        app: vaultaire-db
    spec:
      containers:
      - name: vaultaire-db
        image: mariadb:latest
        env:
          - name: MARIADB_ROOT_PASSWORD
            value: "root"
          - name: MARIADB_DATABASE
            value: "vaultaire"
        ports:
          - containerPort: 3306
        volumeMounts:
          - mountPath: /var/lib/mysql
            name: vaultaire-db-storage
      volumes:
        - name: vaultaire-db-storage
          persistentVolumeClaim:
            claimName: vaultaire-db-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: vaultaire-db
spec:
  selector:
    app: vaultaire-db
  ports:
    - port: 3306
      targetPort: 3306
  type: ClusterIP
```

### Déploiement
```sh
kubectl apply -f ./k8S/vaultaire-db.yaml # toujours l'ancienne version actuellement sur le repo
```



## Partie 8 : Gestion des Services Managés et Résilience


### Résilience et Chaos Engineering

Exemple avec Chaos Mesh :
```sh
# Installation de Chaos Mesh
helm repo add chaos-mesh https://charts.chaos-mesh.org
helm search repo chaos-mesh -l

# Création d'une expérience de chaos (arrêt aléatoire de pods)
kubectl create ns chaos-mesh
helm install chaos-mesh chaos-mesh/chaos-mesh -n=chaos-mesh --set chaosDaemon.runtime=containerd --set chaosDaemon.socketPath=/run/containerd/containerd.sock --version 2.8.0

kubectl get pods -n chaos-mesh -l app.kubernetes.io/instance=chaos-mesh
```


## Partie 9 : Stack de Monitoring avec Prometheus et Grafana

### Déploiement de la Stack de Monitoring
Pour l'observabilité, nous déployons une stack légère Prometheus + Grafana sur Kubernetes.

#### Installation via Helm (recommandé)
```sh
# Ajout du repo Helm
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Installation de kube-prometheus-stack
helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --set grafana.adminPassword='admin'
```

#### Accès aux Interfaces
```sh
# Port-forwarding pour Grafana
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80

# Port-forwarding pour Prometheus
kubectl port-forward -n monitoring svc/monitoring-prometheus 9090:9090
```

### Configuration Métriques
La stack collecte automatiquement les métriques des pods, services et nodes Kubernetes. Nous pouvons ajouter des métriques custom pour Vaultaire en configurant des ServiceMonitors.

```yaml
# Exemple de ServiceMonitor pour Vaultaire
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: vaultaire-monitor
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: vaultaire-ad
  endpoints:
  - port: metrics
    path: /metrics
```