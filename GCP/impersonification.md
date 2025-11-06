

## donner les droit a un user d'usurper un compte de service

```cmd
gcloud iam service-accounts add-iam-policy-binding \
  deploy-automation@tp3-infracloud-m1.iam.gserviceaccount.com \
  --member="user:lorensviguie06@gmail.com" \
  --role="roles/iam.serviceAccountTokenCreator"
```

## impersonifié une commande

```cmd
gcloud auth print-access-token   --impersonate-service-account=deploy-automation@tp3-infracloud-m1.iam.gserviceaccount.com
```