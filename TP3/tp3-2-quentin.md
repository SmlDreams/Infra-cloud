### p2

### Exercice 6  Délégation (Impersonation)

1. creation compte 

```cmd
quentinc33@cloudshell:~/cloudrun-app (tp3-infracloud)$ gcloud iam service-accounts create deploy-automation \
  --display-name="Deploy Automation Service Account"
Created service account [deploy-automation].
```

2. accorder le rôle d'impersonation 

```cmd
quentinc33@cloudshell:~/cloudrun-app (tp3-infracloud)$ gcloud iam service-accounts add-iam-policy-binding deploy-automation@tp3-infracloud.iam.gserviceaccount.com \
  --member="user:quentinc33@yahoo.com" \
  --role="roles/iam.serviceAccountTokenCreator"
Updated IAM policy for serviceAccount [deploy-automation@tp3-infracloud.iam.gserviceaccount.com].
bindings:
- members:
  - user:quentinc33@yahoo.com
  role: roles/iam.serviceAccountTokenCreator
etag: BwZC7ZX2Z7M=
version: 1
```

Quel rôle IAM doit être accordé à votre utilisateur pour lui permettre
dʼexécuter des actions en tant que ce compte ?

roles/iam.serviceAccountTokenCreator

Sur quelle ressource (le compte de service lui-même ou le projet)
cette permission doit-elle être appliquée ?

sur le compte de service pour le principe du moindre privilège.

Pourquoi ne faut-il jamais donner ce rôle à tous les utilisateurs du
projet ?

Ce rôle permet à un utilisateur de se faire passer pour un compte de service, ce qui revient à hériter de tous ses privilèges IAM


3. Tester lʼimpersonation

```cmd
quentinc33@cloudshell:~/cloudrun-app (tp3-infracloud)$ gcloud projects list --impersonate-service-account=deploy-automation@tp3-infracloud.iam.gserviceaccount.com
WARNING: This command is using service account impersonation. All API calls will be executed as [deploy-automation@tp3-infracloud.iam.gserviceaccount.com].
API [cloudresourcemanager.googleapis.com] not enabled on project [572359087531]. Would you like to enable and retry (this will take a few minutes)? (y/N)?  y

Enabling service [cloudresourcemanager.googleapis.com] on project [572359087531]...
WARNING: This command is using service account impersonation. All API calls will be executed as [deploy-automation@tp3-infracloud.iam.gserviceaccount.com].
WARNING: This command is using service account impersonation. All API calls will be executed as [deploy-automation@tp3-infracloud.iam.gserviceaccount.com].
WARNING: This command is using service account impersonation. All API calls will be executed as [deploy-automation@tp3-infracloud.iam.gserviceaccount.com].
Operation "operations/acat.p2-572359087531-9523a5be-5b41-40fd-b998-598981d21d4d" finished successfully.
PROJECT_ID: tp3-infracloud
NAME: tp3-infracloud
PROJECT_NUMBER: 572359087531
```

Quelle option CLI permet de spécifier le compte de service à utiliser
temporairement ?

--impersonate-service-account

Quelles erreurs pouvez-vous rencontrer si la permission est
manquante ou mal configurée ?

permission denied.

4. impersonation avec cloud run 


Dans quel cas pratique une impersonation peut-elle être utilisée lors dʼun déploiement Cloud Run ?

Automatiser un déploiement depuis un pipeline CI/CD

Quelles bonnes pratiques de sécurité sʼappliquent à ce type de délégation ?

Principe du moindre privilège

5. logging 

(pas réussi à trouver de log )

6. Nettoyer la configuration

Retirez la permission dʼimpersonation accordée à votre utilisateur
personnel.

```cmd
quentinc33@cloudshell:~ (tp3-infracloud)$ gcloud iam service-accounts remove-iam-policy-binding deploy-automation@tp3-infracloud.iam.gserviceaccount.com \
  --member="user:quentinc33@yahoo.com" \
  --role="roles/iam.serviceAccountTokenCreator"
Updated IAM policy for serviceAccount [deploy-automation@tp3-infracloud.iam.gserviceaccount.com].
etag: BwZC7elFiNI=
version: 1
```

Pourquoi est-il important de révoquer ce type dʼaccès après usage ?

Respecter le principe du moindre privilège

Quels risques apparaissent si un utilisateur garde la capacité
dʼimpersoner des comptes à privilèges ?

L’utilisateur peut utiliser ce compte pour accéder à d’autres ressources ou services

## Exercice 7. Accès temporaire via IAM Conditions

1. Identifier le cas dʼusage

Vous devez accorder un rôle dʼadministration limité dans le temps
sur votre projet.
Quel rôle IAM accorde des droits complets sur les services Cloud
Run ?

```
roles/run.admin
```

Quel rôle pourrait être utilisé pour une élévation temporaire de
privilège (ex. Compute Admin, Storage Admin, etc.) ?
Choisissez un rôle adapté à votre test.

```
Compute Engine	roles/compute.admin
Cloud Storage	roles/storage.admin
Cloud Functions	roles/cloudfunctions.admin
IAM	            roles/iam.admin
Cloud Build 	roles/cloudbuild.builds.editor
```

pour les tests nous allons utiliser roles/storage.admin

2. Definir la condition temporelle

 Déterminez une date et heure dʼexpiration de lʼaccès (ex. 4 heures à partir de maintenant). Quelle syntaxe CEL permet dʼexprimer cette limite temporelle ? Notez lʼexpression complète de votre condition
```
 request.time < timestamp("2025-11-06T19:35:00Z")
```

3. Creer le rôle conditionel.

Quelle commande permet dʼajouter une attribution de rôle avec une
condition ?

```cmd 
gcloud projects add-iam-policy-binding tp3-infracloud  --member="user:quentinc33@yahoo.com" --role="roles/run.admin" --condition='expression=request.time < timestamp("2025-11-06T19:35:00Z"),title=Expiration4h,description=Accès temporaire Cloud Run pour test'
```

Comment vérifier ensuite que le rôle est bien conditionnel dans la
console IAM ?

rechercher iAM dans la barre de recherche 
trouver l'utilisateur de la commande et regarder l'expiration.

4. Tester lʼaccès avant expiration

```cmd 
quentinc33@cloudshell:~ (tp3-infracloud)$ gcloud run deploy test-service \
  --image=gcr.io/cloudrun/hello \
  --region=europe-west1
Allow unauthenticated invocations to [test-service] (y/N)?  y

Deploying container to Cloud Run service [test-service] in project [tp3-infracloud] region [europe-west1]
Deploying new service...                                                                                                                                                       
  Setting IAM Policy...done                                                                                                                                                    
  Creating Revision...done                                                                                                                                                     
  Routing traffic...done                                                                                                                                                       
Done.                                                                                                                                                                          
Service [test-service] revision [test-service-00001-nfr] has been deployed and is serving 100 percent of traffic.
Service URL: https://test-service-572359087531.europe-west1.run.app
```

Où pouvez-vous vérifier dans la console IAM la présence de la
condition appliquée ?

rechercher iAM dans la barre de recherche 
trouver l'utilisateur de la commande et regarder l'expiration.*


5. Observer le comportement après expiration

Attendez que la date ou lʼheure spécifiée soit dépassée.
Réessayez la même action.
Que se passe-t-il ?

on ne peut plus faire la commade 

Quelle erreur est renvoyée par la CLI ou la console ?

Permissions denied 

Comment ce comportement illustre-t-il le fonctionnement des
conditions IAM ?

le comportement des IAM est dynamique.

6. Nettoyer la configuration

Supprimez le binding conditionnel ou modifiez la condition pour
supprimer la restriction temporelle.

```cmd
gcloud projects remove-iam-policy-binding tp3-infracloud --member="user:quentinc33@yahoo.com" --role="roles/run.admin"
```

### Exercice 8. Auditer les accès et détecter les changements

1. Observer les changements IAM

Filtrez sur les événements de type SetIamPolicy .

Que représentent ces événements ?

Ce log indique que le rôle roles/run.admin avec une condition temporelle a été supprimé pour l’utilisateur quentinc33@yahoo.com

Quelles informations pouvez-vous extraire de leur contenu ?

Utilisateur : quentinc33@yahoo.com
Client OAuth : 618104708054-... (identifie l’outil utilisé)
Adresse IP : 34.22.155.80
Agent utilisateur : gcloud/544.0.0
Horodatage : 2025-11-06T14:47:43Z
Ressource modifiée : projects/tp3-infracloud
Type de ressource : cloudresourcemanager.googleapis.com/Project
Permission utilisée : resourcemanager.projects.setIamPolicy

Quelle ressource a été modifiée en dernier ?

La ressource modifiée en dernier est le projet GCP nommé tp3-infracloud

Comment confirmer que la modification provient bien de votre
utilisateur ?

principalEmail:quentinc33@yahoo.com

3. Analyser les accès Cloud Run
Filtrez les logs du service run.googleapis.com .
Recherchez des actions effectuées par le service Cloud Run associé
au compte run-backend .
Quelles opérations apparaissent ?
Quelle valeur du champ principalEmail prouve que lʼaccès a été effectué
via le compte de service et non un utilisateur humain ?
Quelles permissions Cloud Run ou Storage ont été utilisées ?