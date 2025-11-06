# Bucket Storage 

### 🪣 1. Créer un bucket Cloud Storage
```cmd
gcloud storage buckets create gs://tp3-bucket-p1 \
  --project=tp3-infracloud-m1 \
  --location=EU \
  --uniform-bucket-level-access
```

### 📋 2. Lister les buckets existants dans ton projet

```cmd
gcloud storage buckets list --project=tp3-infracloud-m1
```

### 🔎 3. Voir les détails d’un bucket spécifique

```cmd
gcloud storage buckets describe gs://ynov-tp3-demo
```

### 🗑️ 4. Supprimer un bucket

``cmd
gcloud storage buckets delete gs://ynov-tp3-demo
gcloud storage buckets delete gs://ynov-tp3-demo --quiet
```


### 

```cmd
gcloud storage buckets add-iam-policy-binding gs://tp3-bucket-p1 \
  --member="user:lorensviguie06@gmail.com" \
  --role="roles/storage.objectViewer"

gcloud storage buckets get-iam-policy gs://tp3-bucket-p1 \
  --format="table(bindings.role, bindings.members)"
```