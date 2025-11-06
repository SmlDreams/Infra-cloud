# Compte rendu du TP3

## Exercice 1 . Créer les identités de base

☀️ 1. Création du projet
on a crée un project avec son id et en rajoutant un arguments --name
```cmd
lorensviguie@cloudshell:~$ gcloud projects create tp3-infracloud-m1 --name="TP3 InfraCloud M1"
[...]
Operation "operations/acat.p2-221439700799-73d2cad9-8c2a-4af7-8879-94206b22b353" finished successfully.
```
☀️ 2. Utilisateurs IAM
on ajoute au projet 2 nouveau membre qui sont des comptes google
avec 2 role differnet read only pour lorensviguie06 et un role d'editeur pour lorensvpro
```cmd
lorensviguie@cloudshell:~$ gcloud projects add-iam-policy-binding tp3-infracloud-m1 \
  --member="user:lorensviguie06@gmail.com" \
  --role="roles/viewer"
Updated IAM policy for project [tp3-infracloud-m1].
bindings:
- members:
  - user:lorensviguie@gmail.com
  role: roles/owner
- members:
  - user:Lorensviguie06@gmail.com
  role: roles/viewer
etag: BwZC6RXpqxo=
version: 1
lorensviguie@cloudshell:~$ gcloud projects add-iam-policy-binding tp3-infracloud-m1 \
  --member="user:lorensvpro@gmail.com" \
  --role="roles/editor"
Updated IAM policy for project [tp3-infracloud-m1].
bindings:
- members:
  - user:lorensvpro@gmail.com
  role: roles/editor
- members:
  - user:lorensviguie@gmail.com
  role: roles/owner
- members:
  - user:Lorensviguie06@gmail.com
  role: roles/viewer
etag: BwZC6R2zkhs=
version: 1
```
☀️ 3. Compte de service
on se place dans le projet du tp et on crée un utilisateurs de service pour le moment sans permissions
```cmd
lorensviguie@cloudshell:~$ gcloud config set project  
tp3-infracloud-m1)   tp3-infracloud-m1          
lorensviguie@cloudshell:~$ gcloud config set project tp3-infracloud-m1 
Updated property [core/project].
lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ gcloud iam service-accounts create app-backend   --display-name="Application Backend"
Created service account [app-backend].                     
```
☀️ 4. Vérification
```cmd
lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ gcloud iam service-accounts list
DISPLAY NAME: Application Backend
EMAIL: app-backend@tp3-infracloud-m1.iam.gserviceaccount.com
DISABLED: False
```

## Exercice 2 . Explorer IAM et les rôles

☀️ 1. Lister les membres IAM
on rajoute une permission au compte service juste pour avoir plus de data dans le listing
puis on peut voire les 3 user policy et la policy pour le compte de service 
```cmd
lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ gcloud projects add-iam-policy-binding tp3-infracloud-m1 \
  --member="serviceAccount:app-backend@tp3-infracloud-m1.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.admin"
Updated IAM policy for project [tp3-infracloud-m1].
bindings:
- members:
  - serviceAccount:app-backend@tp3-infracloud-m1.iam.gserviceaccount.com
  role: roles/artifactregistry.admin
- members:
  - user:lorensvpro@gmail.com
  role: roles/editor
- members:
  - user:lorensviguie@gmail.com
  role: roles/owner
- members:
  - user:Lorensviguie06@gmail.com
  role: roles/viewer
etag: BwZC6U_u9Qs=
version: 1

lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ gcloud projects get-iam-policy tp3-infracloud-m1
bindings:
- members:
  - serviceAccount:app-backend@tp3-infracloud-m1.iam.gserviceaccount.com
  role: roles/artifactregistry.admin
- members:
  - user:lorensvpro@gmail.com
  role: roles/editor
- members:
  - user:lorensviguie@gmail.com
  role: roles/owner
- members:
  - user:Lorensviguie06@gmail.com
  role: roles/viewer
etag: BwZC6U_u9Qs=
version: 1
```

## Exercice 3 . Portée des rôles et permissions atomiques

☀️ 1. Comprendre les permissions dʼun rôle
```cmd
lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ gcloud iam roles describe roles/storage.objectViewer
description: Grants access to view objects and their metadata, excluding ACLs. Can
  also list the objects in a bucket.
etag: AA==
includedPermissions:
- resourcemanager.projects.get
- resourcemanager.projects.list
- storage.folders.get
- storage.folders.list
- storage.managedFolders.get
- storage.managedFolders.list
- storage.objects.get
- storage.objects.list
name: roles/storage.objectViewer
stage: GA
title: Storage Object Viewer
```
storage.objects.get	Lire un objet (fichier) dans un bucket.  
storage.objects.list	Lister les objets d’un bucket.  
resourcemanager.projects.get	Lire les informations du projet parent.  
resourcemanager.projects.list	Lister les projets visibles (utile pour navigation IAM).  
storage.folders.get	Permet de lire les métadonnées d’un dossier, par exemple son nom, son parent, ou ses attributs IAM.  
storage.folders.list Permet de lister les dossiers présents à la racine ou dans un sous-dossier.  
storage.managedFolders.get Permet de consulter les informations détaillées d’un dossier géré (Managed Folder).  
storage.managedFolders.list	Permet de lister les Managed Folders enfants d’un bucket ou d’un autre dossier géré.  

☀️ 2. Créer une ressource pour vos tests

je dois liée un billing account pour crée mon bucket
```cmd
lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ gcloud beta billing projects link tp3-infracloud-m1 \
  --billing-account=XXXXXXXXXXXXX
billingAccountName: billingAccounts/XXXXXXXXXXXXX
billingEnabled: true
name: projects/tp3-infracloud-m1/billingInfo
projectId: tp3-infracloud-m1

lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ gcloud storage buckets create gs://tp3-bucket-p1   --project=tp3-infracloud-m1   --location=EU   --uniform-bucket-level-access
Creating gs://tp3-bucket-p1/...

lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ gcloud storage buckets list
---
creation_time: 2025-11-06T09:22:20+0000
default_storage_class: STANDARD
generation: 1762420939780048050
location: EU
location_type: multi-region
metageneration: 1
name: tp3-bucket-p1
public_access_prevention: inherited
rpo: DEFAULT
soft_delete_policy:
  effectiveTime: '2025-11-06T09:22:20.450000+00:00'
  retentionDurationSeconds: '604800'
storage_url: gs://tp3-bucket-p1/
uniform_bucket_level_access: true
update_time: 2025-11-06T09:22:20+0000
```

☀️ 3. Lister les permissions disponibles sur une ressource
```cmd
lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ gcloud iam list-testable-permissions //storage.googleapis.com/projects/_/buckets/tp3-bucket-p1
---
name: resourcemanager.hierarchyNodes.createTagBinding
stage: GA
---
[...]
name: storage.anywhereCaches.create
stage: BETA
title: Create GCS Anywhere Caches
---
name: storage.anywhereCaches.disable
stage: BETA
title: Disable GCS Anywhere Caches
---
name: storage.objects.update
stage: GA
title: Update GCS Object Metadata
```
storage.objects.get	Lire les données et métadonnées d’un objet GCS.  
storage.objects.getIamPolicy	Lire la politique IAM appliquée à l’objet.  
storage.objects.list	Lister les objets présents dans le bucket.  

☀️ 4. Accorder un rôle sur une ressource spécifique
```cmd
lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ gcloud storage buckets add-iam-policy-binding gs://tp3-bucket-p1 \
  --member="user:lorensviguie06@gmail.com" \
  --role="roles/storage.objectViewer"
bindings:
- members:
  - projectEditor:tp3-infracloud-m1
  - projectOwner:tp3-infracloud-m1
  role: roles/storage.legacyBucketOwner
- members:
  - projectViewer:tp3-infracloud-m1
  role: roles/storage.legacyBucketReader
- members:
  - projectEditor:tp3-infracloud-m1
  - projectOwner:tp3-infracloud-m1
  role: roles/storage.legacyObjectOwner
- members:
  - projectViewer:tp3-infracloud-m1
  role: roles/storage.legacyObjectReader
- members:
  - user:Lorensviguie06@gmail.com
  role: roles/storage.objectViewer
etag: CAI=
kind: storage#policy
resourceId: projects/_/buckets/tp3-bucket-p1
version: 1

lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ gcloud storage buckets get-iam-policy gs://tp3-bucket-p1 \
  --format="table(bindings.role, bindings.members)"
ROLE: ['roles/storage.legacyBucketOwner', 'roles/storage.legacyBucketReader', 'roles/storage.legacyObjectOwner', 'roles/storage.legacyObjectReader', 'roles/storage.objectViewer']
MEMBERS: [['projectEditor:tp3-infracloud-m1', 'projectOwner:tp3-infracloud-m1'], ['projectViewer:tp3-infracloud-m1'], ['projectEditor:tp3-infracloud-m1', 'projectOwner:tp3-infracloud-m1'], ['projectViewer:tp3-infracloud-m1'], ['user:Lorensviguie06@gmail.com']]
```
☀️ 5. Tester lʼaccès restreint
```cmd
lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ gcloud auth login lorensviguie06@gmail.com

lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ gcloud storage buckets list
---
creation_time: 2025-11-06T09:22:20+0000
default_storage_class: STANDARD
generation: 1762420939780048050
location: EU
location_type: multi-region
metageneration: 2
name: tp3-bucket-p1
public_access_prevention: inherited
rpo: DEFAULT
soft_delete_policy:
  effectiveTime: '2025-11-06T09:22:20.450000+00:00'
  retentionDurationSeconds: '604800'
storage_url: gs://tp3-bucket-p1/
uniform_bucket_level_access: true
update_time: 2025-11-06T09:45:57+0000
# pour le reste j'ai pas d'object dans le bucket
# mais via la WebUi je ne peux pas push des fichier sur le bukcet mais je le vois bien
# lecture et download marche mais pas push
```
☀️ 6. Étendre le rôle au niveau projet

un peu bête car deja le role view au niveau du projet mais ca marche et permet de donné a un user le droit de vu sur tous les storage bucket du projet
```cmd
lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ gcloud projects add-iam-policy-binding tp3-infracloud-m1 \
  --member="user:lorensviguie06@gmail.com" \
  --role="roles/storage.objectViewer"
Updated IAM policy for project [tp3-infracloud-m1].
bindings:
- members:
  - serviceAccount:app-backend@tp3-infracloud-m1.iam.gserviceaccount.com
  role: roles/artifactregistry.admin
- members:
  - user:lorensvpro@gmail.com
  role: roles/editor
- members:
  - user:lorensviguie@gmail.com
  role: roles/owner
- members:
  - user:Lorensviguie06@gmail.com
  role: roles/storage.objectViewer
- members:
  - user:Lorensviguie06@gmail.com
  role: roles/viewer
etag: BwZC6iyWcUA=
version: 1
```
tjrs que un bucket mais mtn le user si il n'a pas la permission global il pourrai mtn voir tous les bucket du projet et download les bucket et pas faire de modification 

☀️ 7. Comparer les deux portées
Quelles différences observez-vous entre :
    un rôle appliqué sur une ressource spécifique ?
    un rôle appliqué sur un projet entier ?

```txt
un role applique au projet permet d'avoir une visualisation sur l'ensemble du projet exemple quand une nouvelle ressource est crée pas besoin d'allez verifier les permissions utile pour les perssone qui ont besoin d'acces globaux au projet
la ou un rôle sur une ressource precise permet de mieux filtré les acces on limite les acces par groupe ou user permet donc un meilleur filtrage et surtout une meilleur tracabilité 
```

Expliquez en une phrase ce que cela illustre du principe du moindre
privilège ?

```txt
un utilisateur ne dispose des acces en lecture ou ecriture seulement sur les ressources dont il a besoin .

```


☀️ 8. Nettoyer la configuration
```cmd
# on retire la permission au niveau du projet
lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ gcloud projects remove-iam-policy-binding tp3-infracloud-m1 \
  --member="user:Lorensviguie06@gmail.com" \
  --role="roles/storage.objectViewer"
Updated IAM policy for project [tp3-infracloud-m1].
bindings:
- members:
  - serviceAccount:app-backend@tp3-infracloud-m1.iam.gserviceaccount.com
  role: roles/artifactregistry.admin
- members:
  - user:lorensvpro@gmail.com
  role: roles/editor
- members:
  - user:lorensviguie@gmail.com
  role: roles/owner
- members:
  - user:Lorensviguie06@gmail.com
  role: roles/viewer
etag: BwZC6lstEOI=

# on retire la permission au niveau du bucket
lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ gcloud storage buckets remove-iam-policy-binding gs://tp3-bucket-p1   --member="user:Lorensviguie06@gmail.com"   --role="roles/storag
e.objectViewer"
bindings:
- members:
  - projectEditor:tp3-infracloud-m1
  - projectOwner:tp3-infracloud-m1
  role: roles/storage.legacyBucketOwner
- members:
  - projectViewer:tp3-infracloud-m1
  role: roles/storage.legacyBucketReader
- members:
  - projectEditor:tp3-infracloud-m1
  - projectOwner:tp3-infracloud-m1
  role: roles/storage.legacyObjectOwner
- members:
  - projectViewer:tp3-infracloud-m1
  role: roles/storage.legacyObjectReader
etag: CAM=
kind: storage#policy
resourceId: projects/_/buckets/tp3-bucket-p1
version: 1
```
bon la il a encore acces car permission au niveau du projet

## Exercice 4  Créer un rôle personnalisé pour Cloud Run


☀️ 1. Identifier les permissions nécessaires
déployer un service Cloud Run ?
```txt
run.services.create et run.services.update

Permet de créer un nouveau service ou mettre à jour un service existant avec une nouvelle image ou configuration.
```
lister les services existants ?
```txt
un.services.list

Permet de lister tous les services Cloud Run dans un projet ou namespace spécifique.
```
supprimer un service ?
```txt
run.services.delete

Permet de supprimer un service Cloud Run.
```
il existe des rôle prédefinie pour repondre a ces besoin
```txt
roles/run.admin	Toutes les permissions Cloud Run (create, update, delete, list, get, etc.)
roles/run.developer	create, update, get, list (pas delete)
roles/run.viewer get, list seulement (lecture seule)
```

☀️ 2. Créer le fichier de définition

```cmd
# normalement il y a tous les champs obligatoires la
title: "Cloud Run Service Manager"
description: "Rôle personnalisé permettant de créer, lire et supprimer des services Cloud Run"
stage: GA
includedPermissions:
  - run.services.create
  - run.services.get
  - run.services.list
  - run.services.delete
```

☀️ 3. Créer le rôle dans votre projet
```cmd
lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ gcloud iam roles create cloudRunServiceManager \
  --project=tp3-infracloud-m1 \
  --file=test.yaml

WARNING: API is not enabled for permissions: [run.services.create, run.services.get, run.services.list, run.services.delete]. Please enable the corresponding APIs to use those permissions.

Created role [cloudRunServiceManager].
description: Rôle personnalisé permettant de créer, lire et supprimer des services
  Cloud Run
etag: BwZC6pXqsdQ=
includedPermissions:
- run.services.create
- run.services.delete
- run.services.get
- run.services.list
name: projects/tp3-infracloud-m1/roles/cloudRunServiceManager
stage: GA
title: Cloud Run Service Manager

# bon bah on active l'api du coup
lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ gcloud services enable run.googleapis.com
Operation "operations/acf.p2-221439700799-2769e6ac-3833-4c81-8aaf-7a4d13e70ccc" finished successfully.

lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ gcloud iam roles describe cloudRunServiceManager --project=tp3-infracloud-m1
description: Rôle personnalisé permettant de créer, lire et supprimer des services
  Cloud Run
etag: BwZC6pXqsdQ=
includedPermissions:
- run.services.create
- run.services.delete
- run.services.get
- run.services.list
name: projects/tp3-infracloud-m1/roles/cloudRunServiceManager
stage: GA
title: Cloud Run Service Manager
```
☀️ 4. Attribuer le rôle à un utilisateur
```cmd
lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ gcloud projects add-iam-policy-binding tp3-infracloud-m1 \
  --member="user:lorensviguie06@gmail.com" \
  --role="projects/tp3-infracloud-m1/roles/cloudRunServiceManager"
Updated IAM policy for project [tp3-infracloud-m1].
bindings:
- members:
  - user:Lorensviguie06@gmail.com
  role: projects/tp3-infracloud-m1/roles/cloudRunServiceManager
- members:
  - serviceAccount:app-backend@tp3-infracloud-m1.iam.gserviceaccount.com
  role: roles/artifactregistry.admin
- members:
  - serviceAccount:service-221439700799@containerregistry.iam.gserviceaccount.com
  role: roles/containerregistry.ServiceAgent
- members:
  - serviceAccount:221439700799-compute@developer.gserviceaccount.com
  - user:lorensvpro@gmail.com
  role: roles/editor
- members:
  - user:lorensviguie@gmail.com
  role: roles/owner
- members:
  - serviceAccount:service-221439700799@gcp-sa-pubsub.iam.gserviceaccount.com
  role: roles/pubsub.serviceAgent
- members:
  - serviceAccount:service-221439700799@serverless-robot-prod.iam.gserviceaccount.com
  role: roles/run.serviceAgent
- members:
  - user:Lorensviguie06@gmail.com
  role: roles/viewer
etag: BwZC6qxC3-I=
version: 1
```
je suis le compte owner donc j'ai tous les droit sur le projet

☀️ 5. Tester le rôle
```cmd
lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ gcloud config set run/region europe-west9
Updated property [run/region].

lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ gcloud run deploy nginx-test \
  --image=nginx:latest \
  --platform=managed \
  --region=europe-west1 \
  --no-allow-unauthenticated \
  --port 80
Deploying container to Cloud Run service [nginx-test] in project [tp3-infracloud-m1] region [europe-west1]
Deploying new service...                                                                                                                                                           
  Creating Revision...done                                                                                                                                                         
  Routing traffic...done                                                                                                                                                           
Done.   

lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ curl https://nginx-test-221439700799.europe-west1.run.app/
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
[...]
lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ 
Service [nginx-test] revision [nginx-test-00001-jl5] has been deployed and is serving 100 percent of traffic.
Service URL: https://nginx-test-221439700799.europe-west1.run.app

lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ gcloud run services list --region=europe-west1
✔
SERVICE: nginx-test
REGION: europe-west1
URL: https://nginx-test-221439700799.europe-west1.run.app
LAST DEPLOYED BY: lorensviguie@gmail.com
LAST DEPLOYED AT: 2025-11-06T11:03:33.397322Z

lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ gcloud run services delete nginx-test --region=europe-west1
Service [nginx-test] will be deleted.

Do you want to continue (Y/n)?  Y

Deleting [nginx-test]...done.                                                                                                                                                      
Deleted service [nginx-test].
```
tous est passé donc j'ai bien les permission necesaire pour lister crée et delete un container sur cloud run 

☀️ 6. Analyser et corriger
```cmd
#il manque des perm AAAAAAAAAAAAAA
lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ gcloud auth login lorensviguie@gmail.com
[...]
lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ gcloud iam roles update cloudRunServiceManager   --project=tp3-infracloud-m1   --file=test.
[...]
description: Rôle personnalisé permettant de créer, lire et supprimer des services
  Cloud Run
etag: BwZC6uUx8yM=
includedPermissions:
- iam.serviceAccounts.actAs
- run.services.create
- run.services.delete
- run.services.get
- run.services.list
```

☀️ 7. Nettoyer la configuration
```cmd
lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ gcloud iam roles delete cloudRunServiceManager --project=tp3-infracloud-m1
deleted: true
description: Rôle personnalisé permettant de créer, lire et supprimer des services
  Cloud Run
etag: BwZC6xRPQzc=
includedPermissions:
- iam.serviceAccounts.actAs
- run.services.create
- run.services.delete
- run.services.get
- run.services.list
name: projects/tp3-infracloud-m1/roles/cloudRunServiceManager
stage: GA
title: Cloud Run Service Manager
```
Dans quel cas est-il préférable de le retirer plutôt que de le
conserver ?
```txt
si un role de google cloud fait deja ca
si il n'est plus utilisé

role custom plus de maintenance on peut facilement se perdre dans du custom
```

## Exercice 5  Gérer les comptes de service et les droits applicatifs

☀️ 1. Attribuer le rôle approprié

permission :
Lister les objets	storage.objects.list
Lire le contenu d’un objet	storage.objects.get

roles :
storage.objectViewer

```cmd
lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ gcloud storage buckets add-iam-policy-binding gs://tp3-bucket-p1   --member="serviceAccount:app-backend@tp3-infracloud-m1.iam.gservic
eaccount.com"   --role="roles/storage.objectViewer"
bindings:
- members:
  - projectEditor:tp3-infracloud-m1
  - projectOwner:tp3-infracloud-m1
  role: roles/storage.legacyBucketOwner
- members:
  - projectViewer:tp3-infracloud-m1
  role: roles/storage.legacyBucketReader
- members:
  - projectEditor:tp3-infracloud-m1
  - projectOwner:tp3-infracloud-m1
  role: roles/storage.legacyObjectOwner
- members:
  - projectViewer:tp3-infracloud-m1
  role: roles/storage.legacyObjectReader
- members:
  - serviceAccount:app-backend@tp3-infracloud-m1.iam.gserviceaccount.com
  role: roles/storage.objectViewer
etag: CAQ=
kind: storage#policy
resourceId: projects/_/buckets/tp3-bucket-p1
version: 1
lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ 
```
il faut donne le droit que sur le bucket sinon il pourra faire les action du rôle sur tous les bucket

☀️ 2. Préparer lʼapplication à déployer

pour communiquer avec gcloud -> pip install google-cloud-storage
la var d'ENV -> BUCKET_NAME=tp3-bucket-p1
l'auth ce fait vai les Application Default Credentials
[le code](./API/app.py)
```cmd
gcloud iam service-accounts create github-deployer \
  --display-name="GitHub CI/CD Service Account"

gcloud iam service-accounts keys create github-sa-key.json \
  --iam-account=github-deployer@tp3-infracloud-m1.iam.gserviceaccount.com


lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ gcloud projects add-iam-policy-binding tp3-infracloud-m1 \
  --member="serviceAccount:github-deployer@tp3-infracloud-m1.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.admin"
Updated IAM policy for project [tp3-infracloud-m1].
bindings:
- members:
  - serviceAccount:github-deployer@tp3-infracloud-m1.iam.gserviceaccount.com
  role: roles/storage.admin
etag: BwZC7BM1QBE=
version: 1

lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ gcloud projects add-iam-policy-binding tp3-infracloud-m1 \
  --member="serviceAccount:github-deployer@tp3-infracloud-m1.iam.gserviceaccount.com" \
  --role="roles/run.admin"
Updated IAM policy for project [tp3-infracloud-m1)].
bindings:
- members:
  - serviceAccount:976861044501-compute@developer.gserviceaccount.com
  - serviceAccount:976861044501@cloudservices.gserviceaccount.com
  role: roles/editor

lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ gcloud iam service-accounts add-iam-policy-binding 221439700799-compute@developer.gserviceaccount.com   --member="serviceAccount:github-deployer@tp3-infracloud-m1.iam.gserviceaccount.com"   --role="roles/iam.serviceAccountUser"
Updated IAM policy for serviceAccount [221439700799-compute@developer.gserviceaccount.com].
bindings:
- members:
  - serviceAccount:github-deployer@tp3-infracloud-m1.iam.gserviceaccount.com
  role: roles/iam.serviceAccountUser
etag: BwZC7GOf5nM=
version: 1

```
☀️
```cmd

```
☀️
```cmd

```
☀️
```cmd

```
☀️
```cmd

```
☀️
```cmd

```
☀️
```cmd

```
☀️
```cmd

```
