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
circular-truth-477213-d2   tp3-infracloud-m1          
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
