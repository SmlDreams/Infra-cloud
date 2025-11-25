# 4. TP guidé

## 1. Préparation du cloud

Choisir un cloud : GCP
```bash
alexy_daubresse@cloudshell:~$ gcloud projects create infra-cloud-tp4 --name="Role privilege"

alexy_daubresse@cloudshell:~ (infra-cloud-tp4)$ gcloud config get-value project

alexy_daubresse@cloudshell:~ (infra-cloud-tp4)$ gcloud beta billing projects link infra-cloud-tp4 \
  --billing-account=01B893-3D740F-129606

export PROJECT_ID="infra-cloud-tp4"
export REGION="europe-west2"
export ZONE="europe-west2-b"
export VPC_NAME="tp-vpc"
export SUBNET_NAME="tp-subnet-west2"
export SUBNET_RANGE="10.20.0.0/20"
export REPO="tp-app-repo"
export CLUSTER="tp-cluster"


alexy_daubresse@cloudshell:~ (infra-cloud-tp4)$ gcloud services enable \
    compute.googleapis.com \
    container.googleapis.com \
    artifactregistry.googleapis.com
Operation "operations/acf.p2-1073986307428-a028cec5-a4c0-486e-9220-71d50c068eec" finished successfully.

alexy_daubresse@cloudshell:~ (infra-cloud-tp4)$ gcloud compute networks create $VPC_NAME \
    --subnet-mode=custom
Created [https://www.googleapis.com/compute/v1/projects/infra-cloud-tp4/global/networks/tp-vpc].
NAME: tp-vpc
SUBNET_MODE: CUSTOM
BGP_ROUTING_MODE: REGIONAL
IPV4_RANGE: 
GATEWAY_IPV4: 
INTERNAL_IPV6_RANGE: 

Instances on this network will not be reachable until firewall rules
are created. As an example, you can allow all internal traffic between
instances as well as SSH, RDP, and ICMP by running:

$ gcloud compute firewall-rules create <FIREWALL_NAME> --network tp-vpc --allow tcp,udp,icmp --source-ranges <IP_RANGE>
$ gcloud compute firewall-rules create <FIREWALL_NAME> --network tp-vpc --allow tcp:22,tcp:3389,icmp

alexy_daubresse@cloudshell:~ (infra-cloud-tp4)$ gcloud compute networks subnets create $SUBNET_NAME \
  --network=$VPC_NAME \
  --range=$SUBNET_RANGE \
  --region=$REGION
Created [https://www.googleapis.com/compute/v1/projects/infra-cloud-tp4/regions/europe-west2/subnetworks/tp-subnet-west2].
NAME: tp-subnet-west2
REGION: europe-west2
NETWORK: tp-vpc
RANGE: 10.20.0.0/20
STACK_TYPE: IPV4_ONLY
IPV6_ACCESS_TYPE: 
INTERNAL_IPV6_PREFIX: 
EXTERNAL_IPV6_PREFIX: 

alexy_daubresse@cloudshell:~ (infra-cloud-tp4)$ gcloud compute networks list
NAME: default
SUBNET_MODE: AUTO
BGP_ROUTING_MODE: REGIONAL
IPV4_RANGE: 
GATEWAY_IPV4: 
INTERNAL_IPV6_RANGE: 

NAME: tp-vpc
SUBNET_MODE: CUSTOM
BGP_ROUTING_MODE: REGIONAL
IPV4_RANGE: 
GATEWAY_IPV4: 
INTERNAL_IPV6_RANGE: 
```
## 2. Cluster Kubernetes

Créer un cluster managé :

2 nœuds minimum.

Version Kubernetes récente par défaut.Module 10 Kubernetes managé : AKS / EKS / GKE7

```bash
alexy_daubresse@cloudshell:~ (infra-cloud-tp4)$ gcloud container clusters create $CLUSTER \
  --region=$REGION \
  --num-nodes=2 \
  --machine-type=e2-medium \
  --disk-size=50 \
  --enable-autorepair \
  --enable-autoupgrade \
  --network=$VPC_NAME \
  --subnetwork=$SUBNET_NAME
Note: Your Pod address range (`--cluster-ipv4-cidr`) can accommodate at most 1008 node(s).
Creating cluster tp-cluster in europe-west2... Cluster is being health-checked (Kubernetes Control Plane is healthy)...done.                                                                  
Created [https://container.googleapis.com/v1/projects/infra-cloud-tp4/zones/europe-west2/clusters/tp-cluster].
To inspect the contents of your cluster, go to: https://console.cloud.google.com/kubernetes/workload_/gcloud/europe-west2/tp-cluster?project=infra-cloud-tp4
kubeconfig entry generated for tp-cluster.
NAME: tp-cluster
LOCATION: europe-west2
MASTER_VERSION: 1.33.5-gke.1201000
MASTER_IP: 34.147.235.139
MACHINE_TYPE: e2-medium
NODE_VERSION: 1.33.5-gke.1201000
NUM_NODES: 6
STATUS: RUNNING
STACK_TYPE: IPV4
```
* Récupérer la configuration kubeconfig .
```bash
alexy_daubresse@cloudshell:~ (infra-cloud-tp4)$ gcloud container clusters get-credentials $CLUSTER --region=$REGION
Fetching cluster endpoint and auth data.
kubeconfig entry generated for tp-cluster.
```

* Vérifier lʼaccès avec kubectl get nodes .
```bash
alexy_daubresse@cloudshell:~ (infra-cloud-tp4)$ kubectl get nodes
NAME                                        STATUS   ROLES    AGE     VERSION
gke-tp-cluster-default-pool-79302a36-dv5w   Ready    <none>   6m14s   v1.33.5-gke.1201000
gke-tp-cluster-default-pool-79302a36-njf5   Ready    <none>   6m14s   v1.33.5-gke.1201000
gke-tp-cluster-default-pool-969e213b-dd08   Ready    <none>   6m16s   v1.33.5-gke.1201000
gke-tp-cluster-default-pool-969e213b-f5hm   Ready    <none>   6m16s   v1.33.5-gke.1201000
gke-tp-cluster-default-pool-c577045c-rgft   Ready    <none>   6m12s   v1.33.5-gke.1201000
gke-tp-cluster-default-pool-c577045c-xrjz   Ready    <none>   6m13s   v1.33.5-gke.1201000
```

3. Namespace et objets de configuration
* Créer un namespace tp-app .
```bash
alexy_daubresse@cloudshell:~ (infra-cloud-tp4)$ kubectl create namespace tp-app
namespace/tp-app created
```

* Créer un ConfigMap dans tp-app avec au minimum :
APP_MESSAGE (string libre).
UPLOAD_ALLOWED_EXT (ex : .txt ).

```bash
alexy_daubresse@cloudshell:~ (infra-cloud-tp4)$ kubectl create configmap app-config \
  --from-literal=APP_MESSAGE="Bienvenue sur TP Kubernetes !" \
  --from-literal=UPLOAD_ALLOWED_EXT=".txt" \
  -n tp-app
configmap/app-config created
```

* Créer un Secret dans tp-app avec :
UPLOAD_PASSWORD (mot de passe attendu pour lʼupload).

```bash
alexy_daubresse@cloudshell:~ (infra-cloud-tp4)$ kubectl create secret generic app-secret \
  --from-literal=UPLOAD_PASSWORD="MonSuperMDP123" \
  -n tp-app
secret/app-secret created
```

4. Application Python

[APP](./app/)

5. Conteneurisation et registry

* Créer un Dockerfile :
image de base Python officielle,
copie de requirements.txt ,
installation des dépendances,
copie de main.py ,
exposition du port de lʼapp (ex  8000,
commande de démarrage de lʼapp.
* Builder lʼimage Docker en local.
* Tagger lʼimage pour le registry du cloud :
```bash

alexy_daubresse@cloudshell:~ (infra-cloud-tp4)$ gcloud artifacts repositories create tp-app-repo \
  --repository-format=docker \
  --location=europe-west2
Create request issued for: [tp-app-repo]
Waiting for operation [projects/infra-cloud-tp4/locations/europe-west2/operations/c71c82f1-b56a-45ed-b046-965948d40683] to complete...done.                                                   
Created repository [tp-app-repo].

en local

docker tag tp-app-image europe-west2-docker.pkg.dev/infra-cloud-tp4/tp-app-repo/tp-app-image:latest

alexy_daubresse@cloudshell:~ (infra-cloud-tp4)$ gcloud auth configure-docker europe-west2-docker.pkg.dev
```

- Pousser lʼimage dans le registry choisi.

```bash
docker push europe-west2-docker.pkg.dev/infra-cloud-tp4/tp-app-repo/tp-app-image:latest
```

6. Stockage – PVC RWX
* Créer dans le namespace tp-app un PVC nommé shared-pvc avec :
mode dʼaccès : ReadWriteMany ,
taille 1Gi,

[pvc-yml](./yaml/shared-pvc.yaml)

* Vérifier que le PVC passe en état Bound
```bash
alexy_daubresse@cloudshell:~$ gcloud services enable file.googleapis.com --project=infra-cloud-tp4

alexy_daubresse@cloudshell:~$ gcloud filestore instances create tp-filestore \
  --tier=STANDARD \
  --file-share=name="tp_share",capacity=1Gi \
  --network=name="default" \
  --zone=europe-west2-b

alexy_daubresse@cloudshell:~$ kubectl apply -f shared-pvc.yaml

alexy_daubresse@cloudshell:~$ kubectl get pvc -n tp-app
NAME         STATUS   VOLUME        CAPACITY   ACCESS MODES   STORAGECLASS   AGE
shared-pvc   Bound    pvc-9a7c2f8d  1Gi        RWX            nfs-rwx        10s

```

7. Déploiement de lʼapplication
```bash
alexy_daubresse@cloudshell:~$ kubectl get pods -n tp-app
NAME                                 READY   STATUS    RESTARTS   AGE
tp-app-deployment-5c8f9f7b9f-xlj2k   1/1     Running   0          3m
tp-app-deployment-5c8f9f7b9f-vmhpq   1/1     Running   0          3m

```

8. Exposition de lʼapplication
```bash
alexy_daubresse@cloudshell:~$ kubectl get service -n tp-app
NAME            TYPE           CLUSTER-IP      EXTERNAL-IP       PORT(S)        AGE
tp-app-service  LoadBalancer   10.20.35.112    34.38.203.167     80:31414/TCP   5m
```
9. Tests fonctionnels
```bash
alexy_daubresse@cloudshell:~$ curl http://34.38.203.167/
{"app_message":"Bienvenue sur Kubernetes!","files":["lost+found"]}

alexy_daubresse@cloudshell:~$ curl -F "password=MonSuperMDP123" -F "file=@test.txt" http://34.38.203.167/upload
{"message":"File test.txt uploaded successfully"}

alexy_daubresse@cloudshell:~$ curl -F "password=MauvaisMotDePasse" -F "file=@test.txt" http://34.38.203.167/upload
{"error":"Invalid password"}

alexy_daubresse@cloudshell:~$ curl http://34.38.203.167/
{"app_message":"Bienvenue sur Kubernetes!","files":["lost+found","test.txt"]}
```

10. Tests RWX et stateless
```bash
alexy_daubresse@cloudshell:~$ kubectl exec -it tp-app-deployment-5c8f9f7b9f-xlj2k -n tp-app -- /bin/sh
# ls -l /data
total 20
drwx------ 2 root root 16384 Nov 25 10:08 lost+found
-rw-r--r-- 1 root root     4 Nov 25 10:23 test.txt

alexy_daubresse@cloudshell:~$ kubectl exec -it tp-app-deployment-5c8f9f7b9f-vmhpq -n tp-app -- /bin/sh
# ls -l /data
total 20
drwx------ 2 root root 16384 Nov 25 10:08 lost+found
-rw-r--r-- 1 root root     4 Nov 25 10:23 test.txt

alexy_daubresse@cloudshell:~$ kubectl delete pod tp-app-deployment-5c8f9f7b9f-vmhpq -n tp-app
pod "tp-app-deployment-5c8f9f7b9f-vmhpq" deleted

alexy_daubresse@cloudshell:~$ kubectl get pods -n tp-app
NAME                                 READY   STATUS    RESTARTS   AGE
tp-app-deployment-5c8f9f7b9f-rxkpl   1/1     Running   0          20s
tp-app-deployment-5c8f9f7b9f-xlj2k   1/1     Running   0          20m

alexy_daubresse@cloudshell:~$ kubectl exec -it tp-app-deployment-5c8f9f7b9f-rxkpl -n tp-app -- ls -al /data
total 28
drwxr-xr-x 3 root root  4096 Nov 25 10:23 .
drwxr-xr-x 1 root root  4096 Nov 25 10:28 ..
drwx------ 2 root root 16384 Nov 25 10:08 lost+found
-rw-r--r-- 1 root root     4 Nov 25 10:23 test.txt
```

11. Nettoyage
```bash
alexy_daubresse@cloudshell:~$ kubectl delete deployment tp-app-deployment -n tp-app
deployment.apps "tp-app-deployment" deleted

alexy_daubresse@cloudshell:~$ kubectl delete service tp-app-service -n tp-app
service "tp-app-service" deleted

alexy_daubresse@cloudshell:~$ kubectl delete pvc shared-pvc -n tp-app
persistentvolumeclaim "shared-pvc" deleted

alexy_daubresse@cloudshell:~$ kubectl delete configmap app-config -n tp-app
configmap "app-config" deleted

alexy_daubresse@cloudshell:~$ kubectl delete secret app-secret -n tp-app
secret "app-secret" deleted

alexy_daubresse@cloudshell:~$ kubectl delete namespace tp-app
namespace "tp-app" deleted

alexy_daubresse@cloudshell:~$ gcloud container clusters delete tp-cluster --region=europe-west2 --project=infra-cloud-tp4
```