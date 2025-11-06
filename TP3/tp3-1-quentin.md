# Compte rendu du TP3

## Exercice 1 . Créer les identités de base

☀️ 1. Création du projet

```cmd
quentinc33@cloudshell:~ (liquid-sylph-477409-g0)$ gcloud projects create tp3-infracloud \
  --name="tp3-infracloud" \
  --set-as-default
Create in progress for [https://cloudresourcemanager.googleapis.com/v1/projects/tp3-infracloud].
Waiting for [operations/create_project.global.5542707873662098604] to finish...done.                                                                                                                                 
Enabling service [cloudapis.googleapis.com] on project [tp3-infracloud]...
Operation "operations/acat.p2-572359087531-0888f1d1-9afc-489e-8ec1-c8d6b800857f" finished successfully.
Updated property [core/project] to [tp3-infracloud].
```

☀️ 2. Utilisateurs IAM

```cmd
quentinc33@cloudshell:~ (liquid-sylph-477409-g0)$ gcloud projects add-iam-policy-binding tp3-infracloud   --member="user:quentinc33@yahoo.com"   --role="roles/viewer"
Updated IAM policy for project [tp3-infracloud].
bindings:
- members:
  - user:quentinc33@yahoo.com
  role: roles/owner
- members:
  - user:quentinc33@yahoo.com
  role: roles/viewer
etag: BwZC6cagUs4=
version: 1
quentinc33@cloudshell:~ (liquid-sylph-477409-g0)$ gcloud projects add-iam-policy-binding tp3-infracloud   --member="user:lorensvpro@gmail.com"   --role="roles/editor"
Updated IAM policy for project [tp3-infracloud].
bindings:
- members:
  - user:lorensvpro@gmail.com
  role: roles/editor
- members:
  - user:quentinc33@yahoo.com
  role: roles/owner
- members:
  - user:quentinc33@yahoo.com 
  role: roles/viewer
etag: BwZC6c5lN1c=
version: 1
```

☀️ 3. Compte de service

```cmd
quentinc33@cloudshell:~ (liquid-sylph-477409-g0)$ gcloud iam service-accounts create app-backend \
  --display-name="Application Backend"
Created service account [app-backend].                  
```

☀️ 4. Vérification

```cmd
quentinc33@cloudshell:~ (liquid-sylph-477409-g0)$ gcloud iam service-accounts list
DISPLAY NAME: Application Backend
EMAIL: app-backend
```

## Exercice 2 . Explorer IAM et les rôles

☀️ 1.nLister les membres IAM

```cmd
quentinc33@cloudshell:~ (liquid-sylph-477409-g0)$ gcloud projects get-iam-policy tp3-infracloud 
bindings:
- members:
  - user:lorensvpro@gmail.com
  role: roles/editor
- members:
  - user:quentinc33@yahoo.com
  role: roles/owner
- members:
  - user:quentinc33@yahoo.com
  role: roles/viewer
etag: BwZC6c5lN1c=
version: 1
```

## Exercice 3 . Portée des rôles et permissions atomiques
☀️  1. Comprendre les permissions dʼun rôle

```cmd
quentinc33@cloudshell:~ (liquid-sylph-477409-g0)$ gcloud iam roles describe roles/storage.objectViewer
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

resourcemanager.projects.get	Lire les informations du projet parent.  
resourcemanager.projects.list	Lister les projets visibles (utile pour navigation IAM).
storage.folders.get	Permet de lire les métadonnées d’un dossier, par exemple son nom, son parent, ou ses attributs IAM.  
storage.folders.list Permet de lister les dossiers présents à la racine ou dans un sous-dossier. 
storage.managedFolders.get Permet de consulter les informations détaillées d’un dossier géré (Managed Folder).  
storage.managedFolders.list	Permet de lister les Managed Folders enfants d’un bucket ou d’un autre dossier géré.     
storage.objects.get	Lire un objet (fichier) dans un bucket.  
storage.objects.list	Lister les objets d’un bucket.  


☀️ 2. Créer une ressource pour vos tests

```cmd
quentinc33@cloudshell:~ (liquid-sylph-477409-g0)$ gcloud storage buckets create gs://tp3-infracloud-bucket \
  --location=EU
Creating gs://tp3-infracloud-bucket/...
```


☀️ 3. Lister les permissions disponibles sur une ressource

```cmd
quentinc33@cloudshell:~ (liquid-sylph-477409-g0)$ gcloud iam list-testable-permissions //storage.googleapis.com/projects/_/buckets/tp3-infracloud-bucket
```

storage.objects.list permet de lister des objects.
storage.objects.get permet de lire des objects 

☀️ 4. Accorder un rôle sur une ressource spécifique
```cmd
quentinc33@cloudshell:~ (liquid-sylph-477409-g0)$ gcloud storage buckets add-iam-policy-binding gs://tp3-infracloud-bucket \
  --member="user:quentinc33@yahoo.com" \
  --role="roles/storage.objectViewer"
bindings:
- members:
  - projectEditor:liquid-sylph-477409-g0
  - projectOwner:liquid-sylph-477409-g0
  role: roles/storage.legacyBucketOwner
- members:
  - projectViewer:liquid-sylph-477409-g0
  role: roles/storage.legacyBucketReader
- members:
  - user:quentinc33@yahoo.com
  role: roles/storage.objectViewer
etag: CAI=
kind: storage#policy
resourceId: projects/_/buckets/tp3-infracloud-bucket
version: 1
```


☀️ 5. Tester lʼaccès restreint

On peut lister parce que le compte a les permissions storage.objects.list sur ce bucket. mais on ne peut télécharger un objet que si on a le rôle storage.objects.get. On ne peut pas Accéder à un autre bucket du projet car Les permissions sont limitées au bucket d’origine, pas d’accès global au projet.

☀️ 6. Étendre le rôle au niveau projet
```cmd
quentinc33@cloudshell:~ (liquid-sylph-477409-g0)$ gcloud projects add-iam-policy-binding tp3-infracloud \
  --member="user:quentinc33@yahoo.com" \
  --role="roles/storage.objectViewer"
Updated IAM policy for project [tp3-infracloud].
bindings:
- members:
  - user:lorensvpro@gmail.com
  role: roles/editor
- members:
  - user:quentinc33@yahoo.com
  role: roles/owner
- members:
  - user:quentinc33@yahoo.com
  role: roles/storage.objectViewer
- members:
  - user:quentinc33@yahoo.com
  role: roles/viewer
etag: BwZC6keSMcc=
version: 1
```

on peut maintenant acceder à tous les buckets du projets et lister et lire les objets de chaque bucket.

☀️ 7. Comparer les deux portées


Différences :
Portée	                |    Accès accordé	                      |  Exemple                         |
-----------------------------------------------------------------------------------------------------|
Bucket spécifique	    |    Accès limité à un seul bucket	      |  gs://tp3-infracloud-bucket      |
Projet entier	        |    Accès à tous les buckets du projet	  |  gs://bucket1, gs://bucket2, etc.|

Appliquer un rôle sur une ressource spécifique limite les risques en ne donnant que l’accès strictement nécessaire.


☀️ 8. Nettoyer la configuration
```cmd
quentinc33@cloudshell:~ (liquid-sylph-477409-g0)$ gcloud projects remove-iam-policy-binding tp3-infracloud   --member="user:quentinc33@yahoo.com"   --role="roles/storage.objectViewer"
Updated IAM policy for project [tp3-infracloud].
bindings:
- members:
  - user:lorensvpro@gmail.com
  role: roles/editor
- members:
  - user:quentinc33@yahoo.com
  role: roles/owner
- members:
  - user:quentinc33@yahoo.com
  role: roles/viewer
etag: BwZC6lxkl-c=
version: 1
quentinc33@cloudshell:~ (liquid-sylph-477409-g0)$ gcloud storage buckets remove-iam-policy-binding gs://tp3-infracloud-bucket \
  --member="user:quentinc33@yahoo.com" \
  --role="roles/storage.objectViewer"
bindings:
- members:
  - projectEditor:liquid-sylph-477409-g0
  - projectOwner:liquid-sylph-477409-g0
  role: roles/storage.legacyBucketOwner
- members:
  - projectViewer:liquid-sylph-477409-g0
  role: roles/storage.legacyBucketReader
etag: CAM=
kind: storage#policy
resourceId: projects/_/buckets/tp3-infracloud-bucket
version: 1
```
## Exercice 4 . Créer un rôle personnalisé pour Cloud Run

☀️ 1. lister les permissions nécessaires
```cmd
Pour les opérations demandées, voici les permissions spécifiques :
Action	                                Permission requise

Déployer un service	                    run.services.create
Lister les services	                    run.services.list
Supprimer un service	                run.services.delete
lister les détails d'un service         run.services.get
```

☀️ 2. Fichier YAML du rôle personnalisé
```cmd
quentinc33@cloudshell:~ (liquid-sylph-477409-g0)$ cat cloudrun-role.yaml 
title: "CloudRunManager"
description: "Rôle personnalisé pour gérer les services Cloud Run"
stage: "GA"
includedPermissions:
  - run.services.create
  - run.services.list
  - run.services.delete
  - run.services.get

```

☀️3. creer le rôle à partir du yml et vérif 
```cmd
quentinc33@cloudshell:~ (liquid-sylph-477409-g0)$ gcloud iam roles create CloudRunManager --project=tp3-infracloud --file=cloudrun-role.yaml
WARNING: API is not enabled for permissions: [run.services.create, run.services.list, run.services.delete, run.services.get]. Please enable the corresponding APIs to use those permissions.

Created role [CloudRunManager].
description: Rôle personnalisé pour gérer les services Cloud Run
etag: BwZC6qs-LbU=
includedPermissions:
- run.services.create
- run.services.delete
- run.services.get
- run.services.list
name: projects/tp3-infracloud/roles/CloudRunManager
stage: GA
title: CloudRunManager



quentinc33@cloudshell:~ (liquid-sylph-477409-g0)$ gcloud iam roles describe CloudRunManager --project=tp3-infracloud
description: Rôle personnalisé pour gérer les services Cloud Run
etag: BwZC6qs-LbU=
includedPermissions:
- run.services.create
- run.services.delete
- run.services.get
- run.services.list
name: projects/tp3-infracloud/roles/CloudRunManager
stage: GA
title: CloudRunManager
```

☀️ 4. attribuer le rôle à un compte 
```cmd
gcloud projects add-iam-policy-binding tp3-infracloud \
  --member="user:lorensviguie06@gmail.com" \
  --role="projects/tp3-infracloud/roles/CloudRunManager"
```

Pourquoi un autre compte ? Parce que mon compte est owner donc il a tous les droits.

☀️ 5. test des permissions 
```cmd
quentinc33@cloudshell:~ (tp3-infracloud)$ gcloud run services list                                                                            
Listed 0 items.

```

on peut lister les services mais on ne peut pas creer ou delete car il manque une permission (iam.serviceAccounts.actAs )
☀️ 6. Analyser et corriger
```cmd
gcloud iam roles update CloudRunManager   --project=tp3-infracloud --file=cloudrun-role.yaml
```

☀️ 7. netoyage
```cmd
gcloud iam roles delete CloudRunManager --project=tp3-infracloud
```

Il n’est plus utilisé par aucun membre du projet.

Il contient des permissions trop larges ou sensibles.

## Exercice 5. Gérer les comptes de service et les droits applicatifs

☀️ 1.Attribuer le rôle approprié 

Quelle permission permet de lister et lire les objets dʼun bucket Cloud Storage ?

- storage.objects.list → pour lister les objets
- storage.objects.get → pour lire/télécharger les objets

Quel rôle prédéfini contient ces permissions ?

roles/storage.objectViewer

```cmd
quentinc33@cloudshell:~ (tp3-infracloud)$ gcloud iam service-accounts create app-backend \
  --display-name="App Backend Service Account"
Created service account [app-backend].
quentinc33@cloudshell:~ (tp3-infracloud)$ gcloud storage buckets add-iam-policy-binding gs://tp3-infracloud-bucket/   --member="serviceAccount:app-backend@tp3-infracloud.iam.gserviceaccount.com"   --role="roles/storage.objectViewer"
bindings:
- members:
  - projectEditor:tp3-infracloud
  - projectOwner:tp3-infracloud
  role: roles/storage.legacyBucketOwner
- members:
  - projectViewer:tp3-infracloud
  role: roles/storage.legacyBucketReader
- members:
  - serviceAccount:app-backend@tp3-infracloud.iam.gserviceaccount.com
  role: roles/storage.objectViewer
etag: CAQ=
kind: storage#policy
resourceId: projects/_/buckets/tp3-infracloud-bucket
version: 1
```

Accorder ce rôle au niveau du projet donnerait au compte de service accès en lecture à tous les buckets du projet, même ceux qui ne sont pas liés à l’application.

☀️ 
```cmd

```

☀️ 3.Conteneuriser lʼapplication
```cmd
quentinc33@cloudshell:~/cloudrun-app (tp3-infracloud)$ gcloud builds submit --tag gcr.io/tp3-infracloud/cloudrun-app
```

☀️ 4. Déployer sur Cloud Run
```cmd
quentinc33@cloudshell:~/cloudrun-app (tp3-infracloud)$ gcloud run deploy cloudrun-app \
  --image=gcr.io/tp3-infracloud/cloudrun-app \
  --region=europe-west1 \
  --allow-unauthenticated \
  --set-env-vars=BUCKET_NAME=tp3-infracloud-bucket
Deploying container to Cloud Run service [cloudrun-app] in project [tp3-infracloud] region [europe-west1]
Deploying...                                                                                                                                                      
  Setting IAM Policy...done                                                                                                                                       
  Creating Revision...done                                                                                                                                        
  Routing traffic...done                                                                                                                                          
Done.                                                                                                                                                             
Service [cloudrun-app] revision [cloudrun-app-00002-7lw] has been deployed and is serving 100 percent of traffic.
Service URL: https://cloudrun-app-572359087531.europe-west1.run.app
```

Quelle option CLI permet de spécifier le compte de service associé
au déploiement ? 

--service-account

Où pouvez-vous vérifier dans la console que Cloud Run utilise bien
ce compte de service ?

sur ton service,
Onglet "Configuration",
Regarde la section "Compte de service"

☀️ 5.Tester le service
```cmd
quentinc33@cloudshell:~/cloudrun-app (tp3-infracloud)$ curl https://cloudrun-app-572359087531.europe-west1.run.app/list
{"files":[]}
```

Le contenu du bucket sʼaffiche-t-il ?

oui

Que se passe-t-il si le service tente dʼaccéder à un autre bucket
pour lequel il nʼa pas de rôle IAM ?

pas les droits 

Comment ce comportement illustre-t-il le principe du moindre
privilège ?

Le service ne peut accéder qu’aux ressources explicitement autorisées


☀️ 6. logs
```cmd
principalEmail: run-backend@tp3-infracloud.iam.gserviceaccount.com
```

Si le champ principalEmail correspond bien à run-backend@tp3-infracloud.iam.gserviceaccount.com, alors tu as la preuve que c’est ce compte de service qui a effectué la lecture du bucket.

☀️ 7. netoyage

Pourquoi est-il risqué de laisser un compte de service inactif ou
surdimensionné en permissions dans un projet Cloud ?

Escalade de privilèges, Violation du principe du moindre privilège,  Surface d’attaque inutile.
