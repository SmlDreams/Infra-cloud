

## describe un role 

```cmd
gcloud iam roles describe roles/storage.objectViewer
```


### lister les permission

```cmd
gcloud iam list-testable-permissions RESOURCE
gcloud iam list-testable-permissions //storage.googleapis.com/projects/_/buckets/tp3-bucket-p1

gcloud projects get-iam-policy tp3-infracloud-m1 \
  --format="table(bindings.role, bindings.members)"

gcloud storage buckets get-iam-policy tp3-bucket-p1 \
  --format="table(bindings.role, bindings.members)"

```

### retiré un role


niveau d'un projet
```cmd
gcloud projects remove-iam-policy-binding PROJECT_ID \
  --member="user:EMAIL" \
  --role="ROLE"
```

sur un objet precis
```cmd
gcloud storage buckets remove-iam-policy-binding BUCKET_NAME \
  --member="user:EMAIL" \
  --role="ROLE"
```