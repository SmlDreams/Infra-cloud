# Compte rendu du TP3 P1


## Exercice 6 . Délégation (Impersonation)

### ☀️ 1. Créer un nouveau compte de service
Créez un compte de service nommé deploy-automation (ou équivalent).

```bash
lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ gcloud iam service-accounts create deploy-automation \
  --description="Compte de service pour les déploiements automatisés" \
  --display-name="deploy-automation"
Created service account [deploy-automation].
```

### ☀️ 2.Accorder la permission dʼimpersonation

Vous devez autoriser votre compte utilisateur personnel (Gmail) à utiliser le compte de service deploy-automation . 
```bash
lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ gcloud iam service-accounts add-iam-policy-binding \
  deploy-automation@tp3-infracloud-m1.iam.gserviceaccount.com \
  --member="user:lorensviguie06@gmail.com" \
  --role="roles/iam.serviceAccountTokenCreator"
Updated IAM policy for serviceAccount [deploy-automation@tp3-infracloud-m1.iam.gserviceaccount.com].
bindings:
- members:
  - user:Lorensviguie06@gmail.com
  role: roles/iam.serviceAccountTokenCreator
etag: BwZC7Y7rsTk=
version: 1
```

Quel rôle IAM doit être accordé à votre utilisateur pour lui permettre dʼexécuter des actions en tant que ce compte ?  
```bash
roles/iam.serviceAccountTokenCreator
```

Sur quelle ressource (le compte de service lui-même ou le projet) cette permission doit-elle être appliquée ?  
```txt
on le restreint à ce seul compte de service pour limiter la portée du pouvoir.
```

Pourquoi ne faut-il jamais donner ce rôle à tous les utilisateurs du projet ?
```txt
roles/iam.serviceAccountTokenCreator permet de se faire passer pour un compte de service ;

Donc, si quelqu’un peut impersoner deploy-automation, il peut agir avec ses permissions, souvent élevées (ex. déploiement, modification de ressources, accès secrets, etc.) ;
```

### ☀️ 3. Tester lʼimpersonation

```bash
gcloud auth print-access-token   --impersonate-service-account=deploy-automation@tp3-infracloud-m1.iam.gserviceaccount.com
WARNING: This command is using service account impersonation. All API calls will be executed as [deploy-automation@tp3-infracloud-m1.iam.gserviceaccount.com].
ya29.c.c0ASRK0GamzcQg1BjxuAR-1uHPu2azzymBx9duN7YRTgfsv9styQRrYmW0dQa_gA4VWZWbeSyjEvWA__ZftJNYE9IXU198jCqva86f45bUkKXLex823RX_kCT3s_xU_4Q9gUilQgFvm8-jdJlDB0Uy4akjE4G1_2h84ZHLwv4Tv3M6HJ88S0w2YXIWgZhibZFdSnbXZM8ZbjEckhAh90jpdEPMJyIDJOpgwNkaU30O97tA1fXMNbwigSDrhYbaWxVASqbGlsdUJ79eb69F5Fg0sabKXdLVJ_FkyTNuihnsUovERqkbgYujapaAqYIeCXlzofAvisiTnt14IYJBZiWeXUpLfaRMuCLcigs2q33H25iTJRzgKAMOM1MutWvNz_qjLHxNezYk1Pm1y85n0IuTl8D9MsF2Pyf2_iZkVPuYxABbmhxa4ceBTiGcoROer_Iftc6J1GF28U0zxd23sZmSbf3wrUj9Dxtr2FW3a2yM57IElY2gST-hH4sRihRnoOUf0hvOob2Trz0eCQQyJwMjgI-yorJ5OQjQ49W7rqFTRT2gxNSV41uOkTtkHSnnqYUTSccB0L4KUDRqfginuODnI08kLDYvgKPX1-DrqJgUON7fLEN9FOWZ1lQoyTAH644Kxrk1-uOrdV46-qwdWoFXqwqhhrlupRhUsn50bY2z9u6u5aFZQlwfyoIJkfgqeWm663lXdnhOv0Bu4WpUXw86h-2JwpkbFccp3o_Xdh-if2m9zwdBnxtafZ8jVwcgaOBSddaVrkZJSRuJtY3uqQodbfgcaiMdm9l9nS4gWWe1_n9lYczOvmxIq4O_6Ue9eqIYnd-g3Xoe24_f7vflMkbR6VQfivOYewwa045fd_-gh2koBbb9n5ggi02MjeIm_kOZItx6gulnQdtuYMSg7ZVxZjuWfqu9YXsiribwatX85ohWcldUiS7ByQ6t73_XWwp8UOBek8boeXbzS0ZFS0RaMwkt904Mb2vcnOXf4xbF7yo7qZQcY1y7BmZ
```

Quelle option CLI permet de spécifier le compte de service à utiliser temporairement ?  
```bash
--impersonate-service-account=<EMAIL_DU_COMPTE_DE_SERVICE>
```


Exécutez une commande simple (par exemple lister les projets ou les buckets) pour vérifier que lʼimpersonation fonctionne. 
```bash
lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ gcloud projects list \
  --impersonate-service-account=deploy-automation@tp3-infracloud-m1.iam.gserviceaccount.com
WARNING: This command is using service account impersonation. All API calls will be executed as [deploy-automation@tp3-infracloud-m1.iam.gserviceaccount.com].
API [cloudresourcemanager.googleapis.com] not enabled on project [221439700799]. Would you like to enable and retry (this will take a few minutes)? (y/N)?  Y

Enabling service [cloudresourcemanager.googleapis.com] on project [221439700799]...
WARNING: This command is using service account impersonation. All API calls will be executed as

[deploy-automation@tp3-infracloud-m1.iam.gserviceaccount.com].
ERROR: (gcloud.projects.list) PERMISSION_DENIED: Permission denied to enable service [cloudresourcemanager.googleapis.com]
Help Token: AXcLsyB-euLdQsdIw1p_4PSV0_THlv4l6VnF-_XQbcc4nXw1UdOrZ4-7kmdN_4p8M24rI1yF3Cx5U11IJ6Ha-AW6JmdDpAcdUt0z7m5JdczKcNha. This command is authenticated as lorensviguie06@gmail.com which is the active account specified by the [core/account] property. Impersonation is used to impersonate deploy-automation@tp3-infracloud-m1.iam.gserviceaccount.com
- '@type': type.googleapis.com/google.rpc.PreconditionFailure
  violations:
  - subject: '110002'
    type: googleapis.com
- '@type': type.googleapis.com/google.rpc.ErrorInfo
  domain: serviceusage.googleapis.com
  reason: AUTH_PERMISSION_DENIED
lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ gcloud projects list
PROJECT_ID: tp3-infracloud
NAME: tp3-infracloud
PROJECT_NUMBER: 572359087531

PROJECT_ID: tp3-infracloud-m1
NAME: TP3 InfraCloud M1
PROJECT_NUMBER: 221439700799
```

Quelles erreurs pouvez-vous rencontrer si la permission est manquante ou mal configurée ?  
```bash
lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ gcloud auth print-access-token \
  --impersonate-service-account=deploy-automation@tp3-infracloud-m1.iam.gserviceaccount.com
WARNING: This command is using service account impersonation. All API calls will be executed as [deploy-automation@tp3-infracloud-m1.iam.gserviceaccount.com].
ERROR: (gcloud.auth.print-access-token) PERMISSION_DENIED: Failed to impersonate [deploy-automation@tp3-infracloud-m1.iam.gserviceaccount.com]. Make sure the account that's trying to impersonate it has access to the service account itself and the "roles/iam.serviceAccountTokenCreator" role. Permission 'iam.serviceAccounts.getAccessToken' denied on resource (or it may not exist). This command is authenticated as lorensviguie@gmail.com which is the active account specified by the [core/account] property. Impersonation is used to impersonate deploy-automation@tp3-infracloud-m1.iam.gserviceaccount.com. 
- '@type': type.googleapis.com/google.rpc.ErrorInfo
  domain: iam.googleapis.com
  metadata:
    permission: iam.serviceAccounts.getAccessToken
  reason: IAM_PERMISSION_DENIED
```

### ☀️ 4. Utiliser lʼimpersonation avec Cloud Run. 

Dans quel cas pratique une impersonation peut-elle être utilisée lors dʼun déploiement Cloud Run ?
```txt
Tu veux que ton compte utilisateur (toi) ou un pipeline CI/CD (ex: GitHub Actions, GitLab CI, Cloud Build) puisse déployer un service Cloud Run,
mais sans détenir directement les droits d’édition sur le projet.
```

Quelles bonnes pratiques de sécurité sʼappliquent à ce type de délégation ?  
```txt
Utiliser des comptes de service distincts par environnement
Ne jamais stocker de clés de compte de service localement
```
### ☀️ 5. Observer dans les logs

Recherchez les journaux liés à votre action dʼimpersonation. Quels champs du log indiquent :

le compte de service impersonné ?  
```js
principalEmail: "deploy-automation@tp3-infracloud-m1.iam.gserviceaccount.com"
principalSubject: "serviceAccount:deploy-automation@tp3-infracloud-m1.iam.gserviceaccount.com"
```
le compte utilisateur délégant ?  
```json
serviceAccountDelegationInfo: [
0: {
firstPartyPrincipal: {
principalEmail: "Lorensviguie06@gmail.com"
}
}
]
```
Comment ces informations assurent-elles la traçabilité et la non-répudiation ?  
```txt
Comme l’identité de l’utilisateur est loggée au moment de la génération du token, il ne peut pas nier avoir déclenché l’action. Les logs sont horodatés et signés par Cloud Audit Logs, donc non modifiables.
```


### ☀️ 6. Nettoyer la configuration

Retirez la permission dʼimpersonation accordée à votre utilisateur personnel.  
```bash
lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ gcloud iam service-accounts remove-iam-policy-binding   deploy-automation@tp3-infracloud-m1.iam.gserviceaccount.com   --member="user:Lorensviguie06@gmail.com"   --role="roles/iam.serviceAccountTokenCreator"
Updated IAM policy for serviceAccount [deploy-automation@tp3-infracloud-m1.iam.gserviceaccount.com].
etag: BwZC7ekPkzk=
version: 1
```
Pourquoi est-il important de révoquer ce type dʼaccès après usage ?
```txt
si un utilisateur n'a plus besoin d'un droit il ne doit plus l'avoir principe du moindre privilèges
```

Quels risques apparaissent si un utilisateur garde la capacité dʼimpersoner des comptes à privilèges ?
```txt
si on oublie de le retiré et que apres on update les perm du compte de service il peut gagner des permissions qu'il dont il ne  devrait pas a avoir le droit 
```

## Exercice 7 . Accès temporaire via IAM Conditions. 

### ☀️ 1. Identifier le cas dʼusage

Vous devez accorder un rôle dʼadministration limité dans le temps sur votre projet.

Quel rôle IAM accorde des droits complets sur les services Cloud Run ?
```bash
roles/run.admin
```  

Quel rôle pourrait être utilisé pour une élévation temporaire de privilège (ex. Compute Admin, Storage Admin, etc ?  
```txt
Compute Engine	roles/compute.admin	Créer/éditer VM, disques, réseaux
Cloud Storage	roles/storage.admin	Gérer buckets et objets
Cloud SQL	roles/cloudsql.admin	Gérer instances SQL
Cloud Run	roles/run.admin	Déployer et gérer les services Cloud Run
```

Choisissez un rôle adapté à votre test.
```bash
gcloud projects add-iam-policy-binding tp3-infracloud-m1 \
  --member="user:lorensviguie06@gmail.com" \
  --role="roles/run.admin"
# j'ai pas taper la commande c'est pour l'exemple
```

### ☀️ 2. Définir la condition temporelle

Déterminez une date et heure dʼexpiration de lʼaccès (ex. 4 heures àpartir de maintenant).
``txt
originalité 0 -> on va prendre 4h
```

Quelle syntaxe CEL permet dʼexprimer cette limite temporelle ?
```txt
date -u -d "4 hours" +"%Y-%m-%dT%H:%M:%SZ"
```

Notez lʼexpression complète de votre condition.
```yaml
title: "Temporary access 4 hours"
description: "Accès temporaire limité à 4 heures"
expression: "request.time < timestamp('2025-11-06T18:30:00Z')"
```

### ☀️ 3. Créer le rôle conditionnel

Quelle commande permet dʼajouter une attribution de rôle avec une condition ?  
Indiquez :  
le membre = lorensviguie06@gmail.com.  
le rôle choisi = roles/storage.admin.   
lʼexpression CEL = request.time < timestamp("2025-11-06T15:50:00Z").   
un titre et une description pour la condition.  
```bash
lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ gcloud projects add-iam-policy-binding tp3-infracloud-m1 \
  --member="user:lorensviguie06@gmail.com" \
  --role="roles/storage.admin" \
  --condition="title=Temporary bucket admin 5min,description=Accès admin buckets limité à 5 minutes,expression=request.time<timestamp('2025-11-06T15:50:00Z')"
[...]
- condition:
    description: Accès admin buckets limité à 5 minutes
    expression: request.time<timestamp('2025-11-06T15:50:00Z')
    title: Temporary bucket admin 5min
  members:
  - user:Lorensviguie06@gmail.com
  role: roles/storage.admin
- members:
  - user:Lorensviguie06@gmail.com
  role: roles/viewer
etag: BwZC7h9MykU=
version: 3
```

Comment vérifier ensuite que le rôle est bien conditionnel dans la console IAM ?  
```bash
lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ gcloud projects get-iam-policy tp3-infracloud-m1 --format=json
{
  "bindings": [
    [...]
      "role": "roles/run.serviceAgent"
    },
    {
      "condition": {
        "description": "Accès admin buckets limité à 5 minutes",
        "expression": "request.time<timestamp('2025-11-06T15:50:00Z')",
        "title": "Temporary bucket admin 5min"
      },
      "members": [
        "user:Lorensviguie06@gmail.com"
      ],
      "role": "roles/storage.admin"
    },
  ],
  "etag": "BwZC7h9MykU=",
  "version": 3
}
```


### ☀️ 4. Tester lʼaccès avant expiration

```bash
lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ gcloud storage buckets list --project=tp3-infracloud-m1
Listed 0 items.
```

Où pouvez-vous vérifier dans la console IAM la présence de la
condition appliquée ?
```bash
gcloud projects get-iam-policy tp3-infracloud-m1 
```

### ☀️ 5. Observer le comportement après expiration

```bash
lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ gcloud storage buckets list --project=tp3-infracloud-m1
ERROR: (gcloud.storage.buckets.list) PERMISSION_DENIED: The caller does not have permission
```
l'expiration a bien fonctionnée c'est cool

### ☀️ 6. Nettoyer la configuration
```bash
gcloud projects remove-iam-policy-binding tp3-infracloud-m1 \
  --member="user:lorensviguie06@gmail.com" \
  --role="roles/storage.admin" \
  --condition="title=Temporary bucket admin 5min,description=Accès admin buckets limité à 5 minutes,expression=request.time<timestamp('2025-11-06T15:50:00Z')"
```

## Exercice 8 . Auditer les accès et détecter les changements.  


### ☀️ 1. Accéder aux logs

Dans le filtre de recherche, indiquez le service cible. 
```txt
resource.type="cloud_run_revision"
```

Quelle est la différence entre les logs dʼAdmin Activity et ceux de Data Access ?  
```txt
Admin Activity	Actions d’administration et de configuration modifiant les ressources.  
Data Access	Accès aux données utilisateur ou service, lecture/écriture des objets.  
```

Quelles catégories de logs sont activées par défaut sur votre projet ?  
```txt
Admin Activity : ✅ activé par défaut sur toutes les ressources GCP.
System Event : ✅ activé par défaut (logs sur les événements système de GCP, ex. redémarrage de VM).
```
### ☀️ 2. Observer les changements IAM.  

Que représentent ces événements ?
```txt
on voi les events qui sont en lien avec les policy (changement sur les roles permission etc etc ...)
```

Quelles informations pouvez-vous extraire de leur contenu ?
```txt
OHLA beaucoup de chose
mais surtout de qui vient le request quelle perm est affecter et sur quelle user/groupe le changement est fait
et aussi la date
```

Quelle ressource a été modifiée en dernier ?
```txt
storage.admin
```

Comment confirmer que la modification provient bien de votre utilisateur ?
```json
oauthInfo: {1}
principalEmail: "lorensviguie@gmail.com"
principalSubject: "user:lorensviguie@gmail.com"
}
```

### ☀️ 3. Analyser les accès Cloud Run.  
action qui se declenche
```bash
Invoke / Execute
# avec le champ suivants
"principalEmail": "app-backend@tp3-infracloud-m1.iam.gserviceaccount.com"

```
### ☀️ 4. Exporter les logs
```bash
# pour DL
Action download

# pour export vers un bucket
Action Crée un recepteur

# on export les logs?
pour des question de perf de un ca rame de faire des request a l'api direct
et aussi pour pouvoir utiliser des outils plus puissant pour de l'analyse

et aussi pour de la conservation hors site (on adore les norme iso ici)

# l'export
insertId : identifiant unique de la ligne de log puis les champs classique exemple iam en dessous

"protoPayload": {
  "methodName": "google.iam.credentials.v1.IAMCredentials.GenerateAccessToken",
  "serviceName": "iam.googleapis.com",
  "authenticationInfo": {
    "principalEmail": "user@example.com"
  },
  "authorizationInfo": [
    {
      "permission": "iam.serviceAccounts.getAccessToken",
      "granted": true,
      "resource": "projects/_/serviceAccounts/deploy-automation@project.iam.gserviceaccount.com"
    }
  ],
  "request": { ... },
  "response": { ... },
  "serviceData": { ... },
  "resourceName": "projects/_/serviceAccounts/..."
}

```
### ☀️ 5. Créer une alerte

Quelle méthode permet de créer une alerte basée sur un log dans Cloud Monitoring ?  
Filtrez par exemple sur protoPayload.methodName="SetIamPolicy" . 
```txt
Aller dans Logging → Logs-based Metrics → Create Metric
Choisir Counter metric (compte les occurrences)
Aller dans Monitoring → Alerting → Create Policy
```

Quel événement déclencherait cette alerte ?  
```txt
L’alerte se déclenche à chaque modification de politique IAM
```

Quelle notification pouvez-vous configurer ?  
| Type         | Exemple                                                             |
| ------------ | ------------------------------------------------------------------- |
| Email        | Recevoir un email sur un compte administrateur                      |
| SMS / Phone  | Alertes urgentes sur mobile                                         |
| Pub/Sub      | Pour déclencher un workflow automatisé (Cloud Functions, Cloud Run) |
| Webhook      | Appel HTTP vers ton système externe de monitoring ou ticketing      |
| Slack / Chat | Intégration à un canal Slack ou Google Chat                         |

### ☀️ 6. Nettoyer et consigner vos observations

```bash
gcloud logging metrics delete SET_IAM_POLICY_METRIC_NAME
```

[Enregistrez un exemple de log dʼaudit (au format JSON)](./log-IAM.json)
