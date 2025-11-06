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

☀️ 1.nLister les membres IAM
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
