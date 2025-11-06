# Compte rendu du TP3 P1


## Exercice 6  Délégation Impersonation)

☀️ 1. Créer un nouveau compte de service
Créez un compte de service nommé deploy-automation (ou équivalent).

```cmd
lorensviguie@cloudshell:~ (tp3-infracloud-m1)$ gcloud iam service-accounts create deploy-automation \
  --description="Compte de service pour les déploiements automatisés" \
  --display-name="deploy-automation"
Created service account [deploy-automation].
```

☀️ 2.Accorder la permission dʼimpersonation

Vous devez autoriser votre compte utilisateur personnel (Gmail) à utiliser le compte de service deploy-automation . 
```cmd
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
```cmd
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

☀️ 3. Tester lʼimpersonation

```cmd
gcloud auth print-access-token   --impersonate-service-account=deploy-automation@tp3-infracloud-m1.iam.gserviceaccount.com
WARNING: This command is using service account impersonation. All API calls will be executed as [deploy-automation@tp3-infracloud-m1.iam.gserviceaccount.com].
ya29.c.c0ASRK0GamzcQg1BjxuAR-1uHPu2azzymBx9duN7YRTgfsv9styQRrYmW0dQa_gA4VWZWbeSyjEvWA__ZftJNYE9IXU198jCqva86f45bUkKXLex823RX_kCT3s_xU_4Q9gUilQgFvm8-jdJlDB0Uy4akjE4G1_2h84ZHLwv4Tv3M6HJ88S0w2YXIWgZhibZFdSnbXZM8ZbjEckhAh90jpdEPMJyIDJOpgwNkaU30O97tA1fXMNbwigSDrhYbaWxVASqbGlsdUJ79eb69F5Fg0sabKXdLVJ_FkyTNuihnsUovERqkbgYujapaAqYIeCXlzofAvisiTnt14IYJBZiWeXUpLfaRMuCLcigs2q33H25iTJRzgKAMOM1MutWvNz_qjLHxNezYk1Pm1y85n0IuTl8D9MsF2Pyf2_iZkVPuYxABbmhxa4ceBTiGcoROer_Iftc6J1GF28U0zxd23sZmSbf3wrUj9Dxtr2FW3a2yM57IElY2gST-hH4sRihRnoOUf0hvOob2Trz0eCQQyJwMjgI-yorJ5OQjQ49W7rqFTRT2gxNSV41uOkTtkHSnnqYUTSccB0L4KUDRqfginuODnI08kLDYvgKPX1-DrqJgUON7fLEN9FOWZ1lQoyTAH644Kxrk1-uOrdV46-qwdWoFXqwqhhrlupRhUsn50bY2z9u6u5aFZQlwfyoIJkfgqeWm663lXdnhOv0Bu4WpUXw86h-2JwpkbFccp3o_Xdh-if2m9zwdBnxtafZ8jVwcgaOBSddaVrkZJSRuJtY3uqQodbfgcaiMdm9l9nS4gWWe1_n9lYczOvmxIq4O_6Ue9eqIYnd-g3Xoe24_f7vflMkbR6VQfivOYewwa045fd_-gh2koBbb9n5ggi02MjeIm_kOZItx6gulnQdtuYMSg7ZVxZjuWfqu9YXsiribwatX85ohWcldUiS7ByQ6t73_XWwp8UOBek8boeXbzS0ZFS0RaMwkt904Mb2vcnOXf4xbF7yo7qZQcY1y7BmZ
```

Quelle option CLI permet de spécifier le compte de service à utiliser temporairement ?  
```cmd
--impersonate-service-account=<EMAIL_DU_COMPTE_DE_SERVICE>
```


Exécutez une commande simple (par exemple lister les projets ou les buckets) pour vérifier que lʼimpersonation fonctionne. 
```cmd
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
```cmd
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

☀️ 4. Utiliser lʼimpersonation avec Cloud Run. 

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
☀️ 5. Observer dans les logs

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


☀️ 6. Nettoyer la configuration

Retirez la permission dʼimpersonation accordée à votre utilisateur personnel.  
```cmd

```
Pourquoi est-il important de révoquer ce type dʼaccès après usage ?
```txt

```

Quels risques apparaissent si un utilisateur garde la capacité dʼimpersoner des comptes à privilèges ?
```txt

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