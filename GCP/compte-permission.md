## compte de service GitHub

```cmd
gcloud iam service-accounts create github-deployer \
  --display-name="GitHub CI/CD Service Account"

gcloud iam service-accounts keys create github-sa-key.json \
  --iam-account=github-deployer@circular-truth-477213-d2.iam.gserviceaccount.com

```

## compte-utilisateurs
```cmd
# Utilisateur Lecteur (Viewer)
gcloud projects add-iam-policy-binding tp3-infracloud-m1 \
  --member="user:lorensviguie06@gmail.com" \
  --role="roles/viewer"

# Utilisateur Collaborateur (Editor)
gcloud projects add-iam-policy-binding tp3-infracloud-m1 \
  --member="user:lorensvpro@gmail.com" \
  --role="roles/editor"

# Lister tous les membres IAM du projet
gcloud projects get-iam-policy tp3-infracloud-m1
gcloud projects get-iam-policy tp3-infracloud-m1 --format=json
gcloud projects get-iam-policy tp3-infracloud-m1 --format="table(bindings.role, bindings.members)"


# delete un user
gcloud projects remove-iam-policy-binding tp3-infracloud-m1 \
  --member="user:lecteur@example.com" \
  --role="roles/viewer"



```

## Permissions
```cmd

gcloud projects add-iam-policy-binding circular-truth-477213-d2 \
  --member="serviceAccount:github-deployer@circular-truth-477213-d2.iam.gserviceaccount.com" \
  --role="roles/storage.admin"

gcloud projects add-iam-policy-binding circular-truth-477213-d2 \
  --member="serviceAccount:github-deployer@circular-truth-477213-d2.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.admin"


# Rôle permettant de créer et uploader des images dans Artifact Registry
gcloud projects add-iam-policy-binding circular-truth-477213-d2 \
  --member="serviceAccount:github-deployer@circular-truth-477213-d2.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.writer"

# Rôle pour créer, modifier, supprimer les services Cloud Run
gcloud projects add-iam-policy-binding circular-truth-477213-d2 \
  --member="serviceAccount:github-deployer@circular-truth-477213-d2.iam.gserviceaccount.com" \
  --role="roles/run.admin"

# Rôle obligatoire pour utiliser un compte de service lors du déploiement
gcloud projects add-iam-policy-binding circular-truth-477213-d2 \
  --member="serviceAccount:github-deployer@circular-truth-477213-d2.iam.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"

# Option A : sur tout le projet (simple)
gcloud projects add-iam-policy-binding circular-truth-477213-d2 \
  --member="serviceAccount:github-deployer@circular-truth-477213-d2.iam.gserviceaccount.com" \
  --role="roles/storage.admin"


# Option B : sur le bucket seulement (plus sécurisé)
gsutil iam ch \
  serviceAccount:github-deployer@circular-truth-477213-d2.iam.gserviceaccount.com:roles/storage.admin \
  gs://mon-site-web-bucket

# Donne Storage Admin sur un bucket à un compte de service
gcloud storage buckets add-iam-policy-binding gs://mon-site-web-bucket \
    --member="serviceAccount:github-deployer@circular-truth-477213-d2.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

```