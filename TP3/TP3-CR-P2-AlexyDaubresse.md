## Exercice 6  Délégation (Impersonation)

1. Créer un nouveau compte de service

```
alexy_daubresse@cloudshell:~/app (infra-cloud-tp3)$ gcloud iam service-accounts create deploy-automation \
  --description="Compte de service pour les déploiements automatisés" \
  --display-name="deploy-automation"
Created service account [deploy-automation].
```

2. Accorder la permission dʼimpersonation

```
alexy_daubresse@cloudshell:~/app (infra-cloud-tp3)$ gcloud iam service-accounts add-iam-policy-binding \
  deploy-automation@infra-cloud-tp3.iam.gserviceaccount.com \
  --member="user:alexy.daubresse@gmail.com" \
  --role="roles/iam.serviceAccountTokenCreator"
Updated IAM policy for serviceAccount [deploy-automation@infra-cloud-tp3.iam.gserviceaccount.com].
bindings:
- members:
  - user:alexy.daubresse@gmail.com
  role: roles/iam.serviceAccountTokenCreator
etag: BwZC7lVDHdk=
version: 1
```

3. Tester lʼimpersonation

```
alexy_daubresse@cloudshell:~/app (infra-cloud-tp3)$ gcloud auth print-access-token \
  --impersonate-service-account=deploy-automation@infra-cloud-tp3.iam.gserviceaccount.com
WARNING: This command is using service account impersonation. All API calls will be executed as [deploy-automation@infra-cloud-tp3.iam.gserviceaccount.com].
ERROR: (gcloud.auth.print-access-token) PERMISSION_DENIED: Failed to impersonate [deploy-automation@infra-cloud-tp3.iam.gserviceaccount.com].

L’erreur est normale ici : elle indique que la permission iam.serviceAccounts.getAccessToken n’est pas accordée ou mal configurée.
Cela signifie que l’utilisateur n’a pas encore les droits nécessaires pour générer un token au nom de ce compte.
  ```

  4. Utiliser lʼimpersonation avec Cloud Run

  Dans quel cas pratique une impersonation peut-elle être utilisée lors d’un déploiement Cloud Run ?
```
- Lorsqu’un utilisateur ou un pipeline CI/CD (comme Cloud Build, GitHub Actions ou GitLab CI) doit déployer un service Cloud Run,
mais qu’on souhaite éviter de lui accorder directement des droits d’édition sur tout le projet.
L’impersonation permet d’utiliser temporairement un compte de service dédié au déploiement.
```

Quelles bonnes pratiques de sécurité s’appliquent à ce type de délégation ?
```
- Créer et utiliser des comptes de service distincts pour chaque environnement (ex : dev, test, prod)
- Ne jamais stocker de clés de compte de service en local ou dans un dépôt de code
- Limiter les rôles du compte de service au strict nécessaire
- Surveiller et auditer régulièrement l’usage des comptes de service
```

5. Observer dans les logs

Quels champs du log indiquent le compte de service impersonné ?
```
"principalEmail": "deploy-automation@tp3-infracloud-m1.iam.gserviceaccount.com",
"principalSubject": "serviceAccount:deploy-automation@tp3-infracloud-m1.iam.gserviceaccount.com"
```

Quels champs du log indiquent le compte utilisateur délégant ?

```
"serviceAccountDelegationInfo": [
  {
    "firstPartyPrincipal": {
      "principalEmail": "alexyd.dofus1@gmail.com"
    }
  }
]
```
Comment ces informations assurent-elles la traçabilité et la non-répudiation ?
```
Les logs enregistrent à la fois le compte de service utilisé et le compte utilisateur ayant demandé l’action.
Ces journaux sont datés, signés et conservés par Cloud Audit Logs, ce qui rend impossible leur modification.
On peut donc retracer précisément qui a fait quoi, même en cas d’impersonation.
```

6. Nettoyer la configuration
```
gcloud iam service-accounts remove-iam-policy-binding deploy-automation@tp3-infracloud-m1.iam.gserviceaccount.com \
  --member="user:alexy.daubresse@gmail.com" \
  --role="roles/iam.serviceAccountTokenCreator"
```

Pourquoi est-il important de révoquer ce type d’accès après usage ?
```
Pour éviter qu’un utilisateur garde la possibilité de se faire passer pour un compte à privilèges.
Si cette autorisation reste active, elle pourrait être exploitée (volontairement ou non),
créant une faille de sécurité dans le projet.
```
Quels risques apparaissent si un utilisateur garde la capacité d’impersoner des comptes à privilèges ?
```
L’utilisateur pourrait agir avec des permissions élevées sans contrôle,
ce qui peut mener à des modifications non autorisées, des fuites de données, voire des interruptions de service.
Cela augmente aussi les risques en cas de compromission de ce compte utilisateur.
```


## Exercice 7  Accès temporaire via IAM Conditions

1. Identifier le cas dʼusage
Quel rôle IAM accorde des droits complets sur les services Cloud Run ?
```bash
roles/run.admin
```  

Quel rôle pourrait être utilisé pour une élévation temporaire de privilège (ex. Compute Admin, Storage Admin, etc ?  
```txt
Compute Engine  → roles/compute.admin   → Créer / éditer VM, disques, réseaux  
Cloud Storage   → roles/storage.admin   → Gérer buckets et objets  
Cloud SQL       → roles/cloudsql.admin  → Gérer instances SQL  
Cloud Run       → roles/run.admin       → Déployer et gérer les services Cloud Run

```

Choisissez un rôle adapté à votre test.
```bash
gcloud projects add-iam-policy-binding infra-cloud-tp3 \
  --member="user:alexy.daubresse@gmail.com" \
  --role="roles/storage.admin"
```

2. Définir la condition temporelle

Déterminez une date et heure dʼexpiration de lʼaccès (ex. 4 heures àpartir de maintenant).

Quelle syntaxe CEL permet dʼexprimer cette limite temporelle ?
```txt
date -u -d "4 hours" +"%Y-%m-%dT%H:%M:%SZ"
```

Notez lʼexpression complète de votre condition.
```yaml
title: "Temporary access 4 hours"
description: "Accès temporaire limité à 4 heures"
expression: "request.time < timestamp('2025-11-08T22:00:00Z')"
```

3. Créer le rôle conditionnel

Quelle commande permet dʼajouter une attribution de rôle avec une condition ?  
Indiquez :  
le membre = alexy.daubresse@gmail.com  
le rôle choisi = roles/storage.admin.   
lʼexpression CEL = request.time < timestamp("2025-11-06T15:50:00Z").   
un titre et une description pour la condition.  
```bash
gcloud projects add-iam-policy-binding infra-cloud-tp3 \
  --member="user:alexy.daubresse@gmail.com" \
  --role="roles/storage.admin" \
  --condition="title=Temporary bucket admin 5min,description=Accès admin buckets limité à 5 minutes,expression=request.time<timestamp('2025-11-08T19:50:00Z')"

- condition:
    description: Accès admin buckets limité à 5 minutes
    expression: request.time<timestamp('2025-11-08T19:50:00Z')
    title: Temporary bucket admin 5min
  members:
  - user:alexy.daubresse@gmail.com
  role: roles/storage.admin
etag: BwZC8i2AbYw=
version: 3

```

Comment vérifier ensuite que le rôle est bien conditionnel dans la console IAM ?  
```bash
alexy_daubresse@cloudshell:~ (infra-cloud-tp3)$ gcloud projects get-iam-policy infra-cloud-tp3 --format=json

{
  "bindings": [
    {
      "condition": {
        "description": "Accès admin buckets limité à 5 minutes",
        "expression": "request.time<timestamp('2025-11-08T19:50:00Z')",
        "title": "Temporary bucket admin 5min"
      },
      "members": [
        "user:alexy.daubresse@gmail.com"
      ],
      "role": "roles/storage.admin"
    }
  ],
  "etag": "BwZC8i2AbYw=",
  "version": 3
}

```


4. Tester lʼaccès avant expiration

```bash
alexy_daubresse@cloudshell:~ (infra-cloud-tp3)$  gcloud storage buckets list --project=infra-cloud-tp3
Listed 0 items.
```

Où pouvez-vous vérifier dans la console IAM la présence de la
condition appliquée ?
```bash
gcloud projects get-iam-policy infra-cloud-tp3
```

5. Observer le comportement après expiration

```bash
alexy_daubresse@cloudshell:~ (infra-cloud-tp3)$ gcloud storage buckets list --project=infra-cloud-tp3
ERROR: (gcloud.storage.buckets.list) PERMISSION_DENIED: The caller does not have permission

```
l'expiration a bien fonctionnée c'est cool

6. Nettoyer la configuration
```bash
alexy_daubresse@cloudshell:~ (infra-cloud-tp3)$ gcloud projects remove-iam-policy-binding infra-cloud-tp3 \
  --member="user:alexy.daubresse@gmail.com" \
  --role="roles/storage.admin" \
  --condition="title=Temporary bucket admin 5min,description=Accès admin buckets limité à 5 minutes,expression=request.time<timestamp('2025-11-08T19:50:00Z')"
```

## Exercice 8 — Auditer les accès et détecter les changements

1. Accéder aux logs

Dans le filtre de recherche, indiquez le service cible. 

resource.type="cloud_run_revision"


Quelle est la différence entre les logs dʼAdmin Activity et ceux de Data Access ?  
```txt
Admin Activity → actions d’administration ou de configuration qui modifient les ressources  
Data Access → accès aux données utilisateur ou applicatives (lecture / écriture sur les objets)
```

Quelles catégories de logs sont activées par défaut sur votre projet ?  
```txt
Admin Activity : ✅ toujours activé  
System Event : ✅ activé par défaut (événements systèmes automatiques GCP)
Data Access : ❌ désactivé par défaut (à activer manuellement si besoin)

```
2. Observer les changements IAM.  


Quelles informations pouvez-vous extraire de leur contenu ?

- Qui a effectué l’action (compte source)  
- Quelle ressource ou permission a été modifiée  
- À quel moment (horodatage précis)  
- Sur quel compte ou groupe la modification a été appliquée


Quelle ressource a été modifiée en dernier ?
```txt
roles/storage.admin
```

Comment confirmer que la modification provient bien de votre utilisateur ?
```
"authenticationInfo": {
  "principalEmail": "alexy.daubresse@gmail.com",
  "principalSubject": "user:alexy.daubresse@gmail.com"
}
```


3. Analyser les accès Cloud Run.  
action qui se declenche
```
Invoke / Execute
"principalEmail": "app-backend@infra-cloud-tp3.iam.gserviceaccount.com"
```

4. Exporter les logs
```
# Télécharger les logs
Action : Download

# Exporter vers un bucket
Action : Créer un récepteur (sink)


- Pour éviter de saturer les requêtes API lors de grosses analyses  
- Pour conserver les journaux sur un stockage externe (Cloud Storage, BigQuery, Pub/Sub)  
- Pour des besoins de conformité (ISO 27001, RGPD, etc.)  
- Pour croiser les logs avec des outils de SIEM ou d’analyse avancée

"protoPayload": {
  "methodName": "google.iam.credentials.v1.IAMCredentials.GenerateAccessToken",
  "serviceName": "iam.googleapis.com",
  "authenticationInfo": {
    "principalEmail": "alexy.daubresse@gmail.com"
  },
  "authorizationInfo": [
    {
      "permission": "iam.serviceAccounts.getAccessToken",
      "granted": true,
      "resource": "projects/_/serviceAccounts/deploy-automation@infra-cloud-tp3.iam.gserviceaccount.com"
    }
  ],
  "resourceName": "projects/_/serviceAccounts/deploy-automation@infra-cloud-tp3.iam.gserviceaccount.com"
}

```
5. Créer une alerte

Quelle méthode permet de créer une alerte basée sur un log dans Cloud Monitoring ?  
Filtrez par exemple sur protoPayload.methodName="SetIamPolicy" . 
1. Aller dans Logging → Logs-based Metrics → Create Metric  
2. Créer une métrique de type "Counter" avec le filtre :
   protoPayload.methodName="SetIamPolicy"
3. Aller ensuite dans Monitoring → Alerting → Create Policy



Quel événement déclencherait cette alerte ?  

Chaque modification de politique IAM (ajout / suppression / modification de rôles)


Quelle notification pouvez-vous configurer ?  
| Type            | Exemple d’usage                                                      |
| --------------- | -------------------------------------------------------------------- |
| Email           | Envoi automatique à l’équipe d’administration                        |
| SMS / Téléphone | Alerte critique immédiate                                            |
| Pub/Sub         | Déclenchement d’un flux automatisé (Cloud Function, Cloud Run, etc.) |
| Webhook         | Intégration dans un outil de ticketing ou monitoring externe         |
| Slack / Chat    | Notification directe dans un canal d’équipe                          |





6. Nettoyer et consigner vos observations
Nettoyer et consigner vos observations
```
gcloud logging metrics delete SET_IAM_POLICY_METRIC_NAME

gcloud logging read 'protoPayload.methodName="SetIamPolicy"' --limit=1 --format=json > log-iam.json

```