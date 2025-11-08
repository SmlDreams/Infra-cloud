# Compte rendu TP3

## Exercice 1  Créer les identités de base

1. Création du projet
```
alexy_daubresse@cloudshell:~ (circular-truth-477213-d2)$ gcloud projects create infra-cloud-tp3 --name="Role privilege"

Operation "operations/acat.p2-766164356877-93ec633a-5de6-41aa-9517-92ca05eddc15" finished successfully.
```

2. Utilisateurs IAM
Ajoutez deux comptes utilisateur :
```
alexy_daubresse@cloudshell:~ (infra-cloud-tp3)$ gcloud projects add-iam-policy-binding infra-cloud-tp3   --member="user:alexyd.dofus7@gmail.com"   --role="roles/editor"
Updated IAM policy for project [infra-cloud-tp3].
bindings:
- members:
- user:alexyd.dofus7@gmail.com
role: roles/editor
- members:
- user:alexy.daubresse@gmail.com
role: roles/owner
- members:
- user:alexyd.dofus1@gmail.com
role: roles/viewer
etag: BwZC6VG4fAE=
version: 1
```

3. Compte de service
```
alexy_daubresse@cloudshell:~ (infra-cloud-tp3)$ gcloud iam service-accounts create app-backend \
  --display-name="Application backend"
Created service account [app-backend].
```

4. Vérification
```
alexy_daubresse@cloudshell:~ (infra-cloud-tp3)$ gcloud iam service-accounts list
DISPLAY NAME: Application backend
EMAIL: app-backend@infra-cloud-tp3.iam.gserviceaccount.com
DISABLED: False
```

## Exercice 2  Explorer IAM et les rôles

1. Lister les membres IAM
```
alexy_daubresse@cloudshell:~ (infra-cloud-tp3)$ gcloud projects get-iam-policy infra-cloud-tp3 --format=json
{
  "bindings": [
    {
      "members": [
        "user:alexyd.dofus7@gmail.com"
      ],
      "role": "roles/editor"
    },
    {
      "members": [
        "user:alexy.daubresse@gmail.com"
      ],
      "role": "roles/owner"
    },
    {
      "members": [
        "user:alexyd.dofus1@gmail.com"
      ],
      "role": "roles/viewer"
    }
  ],
  "etag": "BwZC6VG4fAE=",
  "version": 1
}
```

## Exercice 3  Portée des rôles et permissions atomiques

1. Comprendre les permissions dʼun rôle
```
alexy_daubresse@cloudshell:~ (infra-cloud-tp3)$ gcloud iam roles describe roles/storage.objectViewer
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

2. Créer une ressource pour vos tests

j'ai du liée mon compte à un billing account pour pouvoir créer mes buckets
```
alexy_daubresse@cloudshell:~ (infra-cloud-tp3)$ gcloud beta billing accounts list
ACCOUNT_ID: 01B893-3D740F-129606
NAME: Mon compte de facturation
OPEN: True
MASTER_ACCOUNT_ID: 

alexy_daubresse@cloudshell:~ (infra-cloud-tp3)$ gcloud beta billing projects link infra-cloud-tp3 \
  --billing-account=01B893-3D740F-129606
billingAccountName: billingAccounts/01B893-3D740F-129606
billingEnabled: true
name: projects/infra-cloud-tp3/billingInfo
projectId: infra-cloud-tp3

alexy_daubresse@cloudshell:~ (infra-cloud-tp3)$ gcloud beta billing projects describe infra-cloud-tp3
billingAccountName: billingAccounts/01B893-3D740F-129606
billingEnabled: true
name: projects/infra-cloud-tp3/billingInfo
projectId: infra-cloud-tp3

alexy_daubresse@cloudshell:~ (infra-cloud-tp3)$ gsutil mb -l europe-west1 gs://infra-cloud-tp3-bucket/
Creating gs://infra-cloud-tp3-bucket/...
```

3. Lister les permissions disponibles sur une ressource
```
alexy_daubresse@cloudshell:~ (infra-cloud-tp3)$ gcloud iam list-testable-permissions //storage.googleapis.com/projects/_/buckets/infra-cloud-tp3-bucket
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
4. Accorder un rôle sur une ressource spécifique
```
alexy_daubresse@cloudshell:~ (infra-cloud-tp3)$ gcloud projects add-iam-policy-binding infra-cloud-tp3   --member="user:alexy.dofus1@gmail.com"   --role="roles/storage.objectViewer"
Updated IAM policy for project [infra-cloud-tp3].
bindings:
- members:
  - user:alexyd.dofus7@gmail.com
  role: roles/editor
- members:
  - user:alexy.daubresse@gmail.com
  role: roles/owner
- members:
  - user:alexy.dofus.1@gmail.com
  role: roles/storage.objectViewer
- members:
  - user:alexyd.dofus1@gmail.com
  role: roles/viewer
etag: BwZC6k9fXnk=
version: 1
```

5. Tester l’accès restreint

J’ai bien accès au bucket, mais comme le bucket est vide et que je n’ai pas les droits de téléchargement/création avec ce compte, c’est normal que je ne puisse rien voir ni modifier pour le moment.
```
alexy_daubresse@cloudshell:~ (infra-cloud-tp3)$ gcloud auth list
Credentialed Accounts

ACTIVE: 
ACCOUNT: alexy.daubresse@gmail.com

ACTIVE: *
ACCOUNT: alexyd.dofus1@gmail.com

alexy_daubresse@cloudshell:~ (infra-cloud-tp3)$ gsutil ls gs://infra-cloud-tp3-bucket/
alexy_daubresse@cloudshell:~ (infra-cloud-tp3)$ gsutil ls -L gs://infra-cloud-tp3-bucket/

alexy_daubresse@cloudshell:~ (infra-cloud-tp3)$ echo "Test fichier" > test.txt
alexy_daubresse@cloudshell:~ (infra-cloud-tp3)$ gsutil cp test.txt gs://infra-cloud-tp3-bucket/
Copying file://test.txt [Content-Type=text/plain]...
AccessDeniedException: 403 alexyd.dofus1@gmail.com does not have storage.objects.create access to the Google Cloud Storage object. Permission 'storage.objects.create' denied on resource (or it may not exist).
```

6. Étendre le rôle au niveau projet

Un peu redondant ici car le rôle Viewer était déjà appliqué au niveau projet, mais cela permet de donner à un utilisateur le droit de voir tous les buckets du projet et de télécharger les objets, sans pouvoir modifier.
```
alexy_daubresse@cloudshell:~ (infra-cloud-tp3)$ gcloud projects add-iam-policy-binding infra-cloud-tp3 \
  --member="user:alexyd.dofus1@gmail.com" \
  --role="roles/storage.objectViewer"
Updated IAM policy for project [infra-cloud-tp3].

alexy_daubresse@cloudshell:~ (infra-cloud-tp3)$ gcloud auth login
alexy_daubresse@cloudshell:~ (infra-cloud-tp3)$ gcloud config set account alexyd.dofus1@gmail.com
alexy_daubresse@cloudshell:~ (infra-cloud-tp3)$ gsutil ls
gs://infra-cloud-tp3-bucket/
alexy_daubresse@cloudshell:~ (infra-cloud-tp3)$ gsutil ls gs://infra-cloud-tp3-bucket/
```
7. Comparer les deux portées

Différences entre un rôle appliqué sur une ressource spécifique et un rôle appliqué sur un projet entier :

Un rôle appliqué au projet donne accès à toutes les ressources du projet (ex: tous les buckets) sans avoir besoin de configurer chaque ressource individuellement.

Un rôle appliqué sur une ressource spécifique permet de limiter les accès précisément à cette ressource (ex: un seul bucket), ce qui améliore la sécurité et la traçabilité.

Principe du moindre privilège résumé en une phrase :

Un utilisateur ne doit disposer que des accès strictement nécessaires pour accomplir ses tâches, ni plus ni moins.

8. Nettoyer la configuration

Pour revenir à une configuration propre, j’ai retiré les rôles IAM ajoutés au niveau projet et au niveau bucket.
```
alexy_daubresse@cloudshell:~ (infra-cloud-tp3)$ gcloud projects remove-iam-policy-binding infra-cloud-tp3 \
  --member="user:alexyd.dofus1@gmail.com" \
  --role="roles/storage.objectViewer"
Updated IAM policy for project [infra-cloud-tp3].

alexy_daubresse@cloudshell:~ (infra-cloud-tp3)$ gsutil iam ch -d user:alexyd.dofus1@gmail.com:objectViewer gs://infra-cloud-tp3-bucket

alexy_daubresse@cloudshell:~ (infra-cloud-tp3)$ gcloud auth login
alexy_daubresse@cloudshell:~ (infra-cloud-tp3)$ gcloud config set account alexyd.dofus1@gmail.com
alexy_daubresse@cloudshell:~ (infra-cloud-tp3)$ gsutil ls gs://infra-cloud-tp3-bucket/
```
## Exercice 4  Créer un rôle personnalisé pour Cloud Run

1. Identifier les permissions nécessaires
déployer un service Cloud Run ?
```
run.services.create et run.services.update

Permet de créer un nouveau service ou mettre à jour un service existant avec une nouvelle image ou configuration.
```
lister les services existants ?
```
un.services.list

Permet de lister tous les services Cloud Run dans un projet ou namespace spécifique.
```
supprimer un service ?
```
run.services.delete

Permet de supprimer un service Cloud Run.
```
il existe des rôle prédefinie pour repondre a ces besoin
```
roles/run.admin	Toutes les permissions Cloud Run (create, update, delete, list, get, etc.)
roles/run.developer	create, update, get, list (pas delete)
roles/run.viewer get, list seulement (lecture seule)
```

2. Créer le fichier de définition

```
title: "Cloud Run Deploy Role"
description: "Rôle personnalisé pour déployer, lister et supprimer des services Cloud Run"
stage: GA
includedPermissions:
  - run.services.create
  - run.services.get
  - run.services.delete
  - run.services.list

```

3. Créer le rôle dans votre projet
```
alexy_daubresse@cloudshell:~ (infra-cloud-tp3)$ gcloud iam roles create cloudRunDeployRole --project=infra-cloud-tp3 --file=cloudrun-custom-role.yaml
WARNING: API is not enabled for permissions: [run.services.create, run.services.get, run.services.delete, run.services.list]. Please enable the corresponding APIs to use those permissions.

Created role [cloudRunDeployRole].
description: Rôle personnalisé pour déployer, lister et supprimer des services Cloud
  Run
etag: BwZC6wjhz4M=
includedPermissions:
- run.services.create
- run.services.delete
- run.services.get
- run.services.list
name: projects/infra-cloud-tp3/roles/cloudRunDeployRole
stage: GA
title: Cloud Run Deploy Role


alexy_daubresse@cloudshell:~ (infra-cloud-tp3)$ gcloud services enable run.googleapis.com --project=infra-cloud-tp3
Operation "operations/acf.p2-766164356877-630ce18f-d6b5-4b63-a6e2-8b71ec213a97" finished successfully.
alexy_daubresse@cloudshell:~ (infra-cloud-tp3)$ gcloud iam roles describe cloudRunDeployRole --project=infra-cloud-tp3
description: Rôle personnalisé pour déployer, lister et supprimer des services Cloud
  Run
etag: BwZC6wjhz4M=
includedPermissions:
- run.services.create
- run.services.delete
- run.services.get
- run.services.list
name: projects/infra-cloud-tp3/roles/cloudRunDeployRole
stage: GA
title: Cloud Run Deploy Role
```

4. Attribuer le rôle à un utilisateur
```
alexy_daubresse@cloudshell:~ (infra-cloud-tp3)$ gcloud projects add-iam-policy-binding infra-cloud-tp3 \
  --member="user:alexyd.dofus1@gmail.com" \
  --role="projects/infra-cloud-tp3/roles/cloudRunDeployRole"
Updated IAM policy for project [infra-cloud-tp3].
bindings:
- members:
  - user:alexyd.dofus1@gmail.com
  role: projects/infra-cloud-tp3/roles/cloudRunDeployRole
- members:
  - serviceAccount:service-766164356877@containerregistry.iam.gserviceaccount.com
  role: roles/containerregistry.ServiceAgent
- members:
  - serviceAccount:766164356877-compute@developer.gserviceaccount.com
  - user:alexyd.dofus7@gmail.com
  role: roles/editor
- members:
  - user:alexy.daubresse@gmail.com
  role: roles/owner
- members:
  - serviceAccount:service-766164356877@gcp-sa-pubsub.iam.gserviceaccount.com
  role: roles/pubsub.serviceAgent
- members:
  - serviceAccount:service-766164356877@serverless-robot-prod.iam.gserviceaccount.com
  role: roles/run.serviceAgent
- members:
  - user:alexyd.dofus1@gmail.com
  role: roles/viewer
etag: BwZC6ykYcoM=
version: 1
```

Parce que ça permet de vérifier que le rôle donne bien les permissions nécessaires sans utiliser ton propre compte qui a souvent plus de droits.

5. Tester le rôle
```
alexy_daubresse@cloudshell:~ (secret-primacy-477408-g5)$ gcloud auth list
Credentialed Accounts

ACTIVE: 
ACCOUNT: alexy.daubresse@gmail.com

ACTIVE: *
ACCOUNT: alexyd.dofus1@gmail.com

To set the active account, run:
    $ gcloud config set account `ACCOUNT`

alexy_daubresse@cloudshell:~ (secret-primacy-477408-g5)$ gcloud run deploy mon-service-test   --image=gcr.io/cloudrun/hello   --region=europe-west1   --project=infra-cloud-tp3   --no-allow-unauthenticated
Deploying container to Cloud Run service [mon-service-test] in project [infra-cloud-tp3] region [europe-west1]
Deploying new service...failed                                                                                                                                                                
Deployment failed                                                                                                                                                                             
ERROR: (gcloud.run.deploy) [alexyd.dofus1@gmail.com] does not have permission to access namespaces instance [infra-cloud-tp3] (or it may not exist): Permission 'iam.serviceaccounts.actAs' denied on service account 766164356877-compute@developer.gserviceaccount.com (or it may not exist). This command is authenticated as alexyd.dofus1@gmail.com which is the active account specified by the [core/account] property.
```

Le rôle personnalisé inclut bien les permissions pour créer, lister et supprimer des services Cloud Run, mais il manque la permission iam.serviceaccounts.actAs qui est nécessaire pour que le compte puisse "agir en tant que" (impersonate) le compte de service associé au déploiement Cloud Run.


6. Analyser et corriger

```
includedPermissions:
- run.services.create
- run.services.delete
- run.services.get
- run.services.list
- iam.serviceAccounts.actAs

alexy_daubresse@cloudshell:~ (infra-cloud-tp3)$ gcloud iam roles update cloudRunDeployRole --project=infra-cloud-tp3 --file=/home/alexy_daubresse/cloudrun-custom-role.yaml
The specified role does not contain an "etag" field identifying a specific version to replace. Updating a role without an "etag" can overwrite concurrent role changes.

Replace existing role (Y/n)?  Y

description: Rôle personnalisé pour déployer, lister et supprimer des services Cloud
  Run
etag: BwZC7CTe7lc=
includedPermissions:
- iam.serviceAccounts.actAs
- run.services.create
- run.services.delete
- run.services.get
- run.services.list
name: projects/infra-cloud-tp3/roles/cloudRunDeployRole
stage: GA
title: Cloud Run Deploy Role
alexy_daubresse@cloudshell:~ (infra-cloud-tp3)$ gcloud auth login alexyd.dofus1@gmail.com

You are already authenticated with gcloud when running
inside the Cloud Shell and so do not need to run this
command. Do you wish to proceed anyway?

Do you want to continue (Y/n)?  Y

WARNING: Re-using locally stored credentials for [alexyd.dofus1@gmail.com]. To fetch new credentials, re-run the command with the `--force` flag.

You are now logged in as [alexyd.dofus1@gmail.com].
Your current project is [infra-cloud-tp3].  You can change this setting by running:
  $ gcloud config set project PROJECT_ID
alexy_daubresse@cloudshell:~ (infra-cloud-tp3)$ gcloud run deploy mon-service-test   --image=gcr.io/cloudrun/hello   --region=europe-west1   --project=infra-cloud-tp3   --no-allow-unauthenticated
Deploying container to Cloud Run service [mon-service-test] in project [infra-cloud-tp3] region [europe-west1]
Deploying new service...                                                                                                                                                                      
  Creating Revision...done                                                                                                                                                                    
  Routing traffic...done                                                                                                                                                                      
Done.                                                                                                                                                                                         
Service [mon-service-test] revision [mon-service-test-00001-9mg] has been deployed and is serving 100 percent of traffic.
Service URL: https://mon-service-test-766164356877.europe-west1.run.app
```

7. Nettoyer la configuration

```
alexy_daubresse@cloudshell:~ (infra-cloud-tp3)$ gcloud projects remove-iam-policy-binding infra-cloud-tp3 \
  --member="user:alexyd.dofus1@gmail.com" \
  --role="projects/infra-cloud-tp3/roles/cloudRunDeployRole"
Updated IAM policy for project [infra-cloud-tp3].
bindings:
- members:
  - serviceAccount:service-766164356877@containerregistry.iam.gserviceaccount.com
  role: roles/containerregistry.ServiceAgent
- members:
  - serviceAccount:766164356877-compute@developer.gserviceaccount.com
  - user:alexyd.dofus7@gmail.com
  role: roles/editor
- members:
  - user:alexy.daubresse@gmail.com
  role: roles/owner
- members:
  - serviceAccount:service-766164356877@gcp-sa-pubsub.iam.gserviceaccount.com
  role: roles/pubsub.serviceAgent
- members:
  - serviceAccount:service-766164356877@serverless-robot-prod.iam.gserviceaccount.com
  role: roles/run.serviceAgent
- members:
  - user:alexyd.dofus1@gmail.com
  role: roles/viewer
etag: BwZC7DZ38oQ=
version: 1
alexy_daubresse@cloudshell:~ (infra-cloud-tp3)$ gcloud projects get-iam-policy infra-cloud-tp3
bindings:
- members:
  - serviceAccount:service-766164356877@containerregistry.iam.gserviceaccount.com
  role: roles/containerregistry.ServiceAgent
- members:
  - serviceAccount:766164356877-compute@developer.gserviceaccount.com
  - user:alexyd.dofus7@gmail.com
  role: roles/editor
- members:
  - user:alexy.daubresse@gmail.com
  role: roles/owner
- members:
  - serviceAccount:service-766164356877@gcp-sa-pubsub.iam.gserviceaccount.com
  role: roles/pubsub.serviceAgent
- members:
  - serviceAccount:service-766164356877@serverless-robot-prod.iam.gserviceaccount.com
  role: roles/run.serviceAgent
- members:
  - user:alexyd.dofus1@gmail.com
  role: roles/viewer
etag: BwZC7DZ38oQ=
version: 1
```

## Exercice 5  Gérer les comptes de service et les droits applicatifs

1. Attribuer le rôle approprié

Quelles permissions permettent de lister et lire les objets d’un bucket Cloud Storage ?

storage.objects.list → pour lister les objets

storage.objects.get → pour lire / télécharger les objets

```
alexy_daubresse@cloudshell:~ (infra-cloud-tp3)$ gcloud iam service-accounts create app-backend \
  --display-name="App Backend Service Account"
Created service account [app-backend].

alexy_daubresse@cloudshell:~ (infra-cloud-tp3)$ gcloud storage buckets add-iam-policy-binding gs://infra-cloud-tp3-bucket/ \
  --member="serviceAccount:app-backend@infra-cloud-tp3.iam.gserviceaccount.com" \
  --role="roles/storage.objectViewer"
```

3. Conteneuriser l’application

```
alexy_daubresse@cloudshell:~/app (infra-cloud-tp3)$ gcloud builds submit --tag gcr.io/infra-cloud-tp3/cloudrun-app
```

4. Déployer sur Cloud Run

```
alexy_daubresse@cloudshell:~/app (infra-cloud-tp3)$ gcloud run deploy cloudrun-app \
  --image=gcr.io/infra-cloud-tp3/cloudrun-app \
  --region=europe-west1 \
  --allow-unauthenticated \
  --set-env-vars=BUCKET_NAME=infra-cloud-tp3-bucket
```

Quelle option permet de spécifier le compte de service utilisé ?

--service-account

Où vérifier dans la console ?
Dans l’onglet Configuration du service Cloud Run, section Compte de service.

5. Tester le service

```
alexy_daubresse@cloudshell:~/app (infra-cloud-tp3)$ curl https://cloudrun-app-21039605774.europe-west1.run.app/list
{"files":[]}
```

Le contenu du bucket s’affiche-t-il ?
Oui, les fichiers du bucket sont bien listés.

Que se passe-t-il si le service tente d’accéder à un autre bucket sans droit IAM ?
L’accès est refusé : le service n’a pas les permissions nécessaires.

Comment cela illustre-t-il le principe du moindre privilège ?
Le service ne peut accéder qu’aux ressources explicitement autorisées, limitant les risques d’abus ou d’erreurs.

6. Observer les logs

```
"principalEmail": "app-backend@infra-cloud-tp3.iam.gserviceaccount.com"
```

7. Nettoyage
```
gcloud iam service-accounts delete app-backend@infra-cloud-tp3.iam.gserviceaccount.com
```

Pourquoi est-il risqué de laisser un compte de service inactif ou surdimensionné en permissions ?

Risque d’escalade de privilèges

Violation du principe du moindre privilège

Surface d’attaque inutile en cas de compromission

Il est donc recommandé de supprimer les comptes de service inutilisés ou de réduire leurs droits au strict nécessaire.