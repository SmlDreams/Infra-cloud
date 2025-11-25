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

```cmd
docker tag tp-app:latest europe-west1-docker.pkg.dev/lorens060104/tp-app-repo/tp-app:latest
docker push europe-west1-docker.pkg.dev/lorens060104/tp-app-repo/tp-app:latest

```

```cmd
gcloud artifacts repositories create tp-app-repo \
  --repository-format=docker \
  --location=europe-west1
gcloud auth configure-docker europe-west1-docker.pkg.dev
gcloud artifacts docker images list europe-west1-docker.pkg.dev/lorens060104/tp-app-repo
```

## 6. Stockage – PVC RWX

[pvc-yml](./yaml/shared-pvc.yaml)

```cmd
gcloud services enable file.googleapis.com --project=lorens060104
gcloud filestore instances create tp-filestore \
  --tier=STANDARD \
  --file-share=name="tp_share",capacity=1024GiB \
  --network=name="default" \
  --zone=europe-west1-b
kubectl apply -f shared-pvc.yaml
kubectl get pvc -n tp-app
NAME         STATUS   VOLUME      CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
shared-pvc   Bound    shared-pv   1Gi        RWX            nfs-rwx        <unset>                 4s
```

## 7. Déploiement de lʼapplication

```cmd
kubectl get pods -n tp-app
NAME                                 READY   STATUS    RESTARTS   AGE
tp-app-deployment-7994dd448f-n2crq   1/1     Running   0          2m55s
tp-app-deployment-7994dd448f-zcqtf   1/1     Running   0          2m55s
```

## 8. Exposition de lʼapplication

```cmd
kubectl get service -n tp-app
NAME             TYPE           CLUSTER-IP      EXTERNAL-IP     PORT(S)        AGE
tp-app-service   LoadBalancer   34.118.231.30   34.38.203.167   80:31414/TCP   3m51s
```

## 9. Tests fonctionnels

```cmd
curl http://34.38.203.167/
{"app_message":"Hello from Kubernetes!","files":["lost+found"]}
curl -F "password=MonSuperMotDePasse123" -F "file=@test.txt" http://34.38.203.167/upload
{"message":"File test.txt uploaded successfully"}
curl -F "password=SuperMotDePasse123" -F "file=@test.txt" http://34.38.203.167/upload
{"error":"Invalid password"}
curl http://34.38.203.167/
{"app_message":"Hello from Kubernetes!","files":["lost+found","test.txt"]}
```

## 10. Tests RWX et stateless

```cmd
kubectl exec -it tp-app-deployment-7994dd448f-n2crq -n tp-app -- /bin/sh
# ls -l /data
total 20
drwx------ 2 root root 16384 Nov 25 10:08 lost+found
-rw-r--r-- 1 root root     4 Nov 25 10:23 test.txt
kubectl exec -it tp-app-deployment-7994dd448f-zcqtf -n tp-app -- /bin/sh
# ls -l /data
total 20
drwx------ 2 root root 16384 Nov 25 10:08 lost+found
-rw-r--r-- 1 root root     4 Nov 25 10:23 test.txt

kubectl delete pod tp-app-deployment-7994dd448f-zcqtf -n tp-app
pod "tp-app-deployment-7994dd448f-zcqtf" deleted from tp-app namespace
kubectl get pods -n tp-app
NAME                                 READY   STATUS        RESTARTS   AGE
tp-app-deployment-7994dd448f-2j8d9   1/1     Running       0          15s
tp-app-deployment-7994dd448f-n2crq   1/1     Running       0          16m
tp-app-deployment-7994dd448f-zcqtf   1/1     Terminating   0          16m

kubectl exec -it tp-app-deployment-7994dd448f-2j8d9 -n tp-app -- ls -al /data
total 28
drwxr-xr-x 3 root root  4096 Nov 25 10:23 .
drwxr-xr-x 1 root root  4096 Nov 25 10:28 ..
drwx------ 2 root root 16384 Nov 25 10:08 lost+found
-rw-r--r-- 1 root root     4 Nov 25 10:23 test.txt
```

## 11. Nettoyage

```cmd
kubectl delete deployment tp-app-deployment -n tp-app
kubectl delete service tp-app-service -n tp-app
kubectl delete pvc shared-pvc -n tp-app
kubectl delete configmap app-config -n tp-app
kubectl delete secret app-secret -n tp-app
kubectl delete namespace tp-app

gcloud container clusters delete tp4-kubcluster --zone=europe-west1-b --project=lorens060104
gcloud artifacts repositories delete tp-app-repo --location=europe-west1 --project=lorens060104

```