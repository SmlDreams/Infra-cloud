# Compte rendu TP4 Partie 2

## Sécurité opérationnelle Kubernetes

```sh
MacBook-Air-de-Remult:yaml remult$kubectl get clusterrolebindings | grep cluster-admin
cluster-admin                                                   ClusterRole/cluster-admin                                                          25m
kubeadm:cluster-admins                                          ClusterRole/cluster-admin                                                          25m

MacBook-Air-de-Remult:yaml remult$kubectl auth can-i list pods -n dev --as=bob
no
MacBook-Air-de-Remult:yaml remult$kubectl auth can-i list pods -n kube-system --as=bob
no

# create a custom role

MacBook-Air-de-Remult:yaml remult$ kubectl apply -f role-pod-reader.yaml 
role.rbac.authorization.k8s.io/pod-reader created
MacBook-Air-de-Remult:yaml remult$ kubectl apply -f rb-pod-reader-bob.yaml 
rolebinding.rbac.authorization.k8s.io/pod-reader-bob created
MacBook-Air-de-Remult:yaml remult$ kubectl auth can-i list pods -n dev --as=bob
yes

#create admin role for ns
MacBook-Air-de-Remult:yaml remult$ kubectl apply -f rb-dev-admin-alice.yaml 
rolebinding.rbac.authorization.k8s.io/dev-admin-alice created
MacBook-Air-de-Remult:yaml remult$ kubectl auth can-i list pods -n dev --as=alice
yes
MacBook-Air-de-Remult:yaml remult$ kubectl auth can-i list pods -n prod --as=alice
no

# Pod security
MacBook-Air-de-Remult:yaml remult$ kubectl label namespace dev \
>   pod-security.kubernetes.io/enforce=baseline \
>   pod-security.kubernetes.io/enforce-version=v1.30 --overwrite
namespace/dev labeled
MacBook-Air-de-Remult:yaml remult$ kubectl label namespace prod \
>   pod-security.kubernetes.io/enforce=restricted \
>   pod-security.kubernetes.io/enforce-version=v1.30 --overwrite
namespace/prod labeled

MacBook-Air-de-Remult:yaml remult$ kubectl apply -f insecure-pod.yaml -n prod
Error from server (Forbidden): error when creating "insecure-pod.yaml": pods "insecure-pod" is forbidden: violates PodSecurity "restricted:v1.30": host namespaces (hostNetwork=true), privileged (container "evil" must not set securityContext.privileged=true), allowPrivilegeEscalation != false (container "evil" must set securityContext.allowPrivilegeEscalation=false), unrestricted capabilities (container "evil" must set securityContext.capabilities.drop=["ALL"]), runAsNonRoot != true (pod or container "evil" must set securityContext.runAsNonRoot=true), seccompProfile (pod or container "evil" must set securityContext.seccompProfile.type to "RuntimeDefault" or "Localhost")


# Durcir un Pod pour satisfaire le profil restricted
MacBook-Air-de-Remult:yaml remult$ kubens dev
Context "docker-desktop" modified.
Active namespace is "dev".
MacBook-Air-de-Remult:yaml remult$ kubectl get pods
NAME        READY   STATUS    RESTARTS   AGE
nginx-dev   1/1     Running   0          15s
MacBook-Air-de-Remult:yaml remult$ kubens prod
Context "docker-desktop" modified.
Active namespace is "prod".
MacBook-Air-de-Remult:yaml remult$ kubectl get pods
NAME                READY   STATUS             RESTARTS     AGE
nginx-prod-secure   0/1     CrashLoopBackOff   1 (6s ago)   21s

# Étude d’un ServiceAccount sur-privilégié

MacBook-Air-de-Remult:yaml remult$ kubectl apply -f serviceAccount.yaml 
serviceaccount/sa-risky created
clusterrolebinding.rbac.authorization.k8s.io/crb-sa-risky created
MacBook-Air-de-Remult:yaml remult$ kubectl get pods
NAME         READY   STATUS    RESTARTS   AGE
hacker-pod   1/1     Running   0          38s
nginx-dev    1/1     Running   0          9m4s
MacBook-Air-de-Remult:yaml remult$ kubectl exec -it hacker-pod -- kubectl get pods
NAME         READY   STATUS    RESTARTS   AGE
hacker-pod   1/1     Running   0          73s
nginx-dev    1/1     Running   0          9m39s
MacBook-Air-de-Remult:yaml remult$ kubectl delete -f serviceAccount.yaml 
serviceaccount "sa-risky" deleted from dev namespace
clusterrolebinding.rbac.authorization.k8s.io "crb-sa-risky" deleted
MacBook-Air-de-Remult:yaml remult$ kubectl get pods
NAME         READY   STATUS    RESTARTS   AGE
hacker-pod   1/1     Running   0          106s
nginx-dev    1/1     Running   0          10m
MacBook-Air-de-Remult:yaml remult$ kubectl exec -it hacker-pod -- kubectl get pods
error: You must be logged in to the server (Unauthorized)
command terminated with exit code 1

# Diagnostiquer un refus Pod Security

```

## CI/CD, Helm et GitOps sur Kubernetes

```sh
#  Installer Argo CD dans le cluster
MacBook-Air-de-Remult:yaml remult$ kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
customresourcedefinition.apiextensions.k8s.io/applications.argoproj.io unchanged
[...]
networkpolicy.networking.k8s.io/argocd-server-network-policy created

#  Accéder à l’interface Argo CD
MacBook-Air-de-Remult:yaml remult$ kubectl port-forward svc/argocd-server -n argocd 8080:443
Forwarding from 127.0.0.1:8080 -> 8080
Forwarding from [::1]:8080 -> 8080
### passwd argo jCwANePmlc3IzFwf

# Créer un chart Helm minimal pour l’application guestbook
MacBook-Air-de-Remult:helm-work remult$ helm create guestbook
Creating guestbook

# Tester manuellement le chart Helm

MacBook-Air-de-Remult:helm-work remult$ export POD_NAME=$(kubectl get pods -n guestbook -l "app.kubernetes.io/name=guestbook,app.kubernetes.io/instance=guestbook" -o jsonpath="{.items[0].metadata.name}")
MacBook-Air-de-Remult:helm-work remult$ export CONTAINER_PORT=$(kubectl get pod -n guestbook $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
MacBook-Air-de-Remult:helm-work remult$ kubectl -n guestbook port-forward $POD_NAME 8081:$CONTAINER_PORT
Forwarding from 127.0.0.1:8081 -> 5678
Forwarding from [::1]:8081 -> 5678

MacBook-Air-de-Remult:Infra-cloud remult$ curl localhost:8081
Hello from guestbook

MacBook-Air-de-Remult:Infra-cloud remult$ helm uninstall guestbook -n guestbook
release "guestbook" uninstalled

## Définir l’ Application Argo CD
bon je vais pas mettre des screen mais ca marche
MacBook-Air-de-Remult:Infra-cloud remult$ kubectl get service
NAME        TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE
guestbook   ClusterIP   10.110.204.217   <none>        80/TCP    119s
MacBook-Air-de-Remult:Infra-cloud remult$ kubectl get service
NAME        TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE
guestbook   ClusterIP   10.110.204.217   <none>        800/TCP   3m18s


## les divergences

MacBook-Air-de-Remult:Infra-cloud remult$ kubectl scale deployment guestbook --replicas=5 -n guestbook
deployment.apps/guestbook scaled
MacBook-Air-de-Remult:Infra-cloud remult$ kubectl get deployment -n guestbook
NAME        READY   UP-TO-DATE   AVAILABLE   AGE
guestbook   1/1     5            1           5m23s
MacBook-Air-de-Remult:Infra-cloud remult$ kubectl get deployment -n guestbook
NAME        READY   UP-TO-DATE   AVAILABLE   AGE
guestbook   1/1     1            1           6m33s
```

