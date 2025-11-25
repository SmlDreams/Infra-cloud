

gcloud container clusters create CLUSTER_NAME [OPTIONS...]

```cmd
gcloud container clusters create tp4Kubcluster \
  --zone=europe-west1-b \
  --machine-type=e2-medium \
  --num-nodes=2 \
  --project=lorens060104
```


| Flag                | Description                            |
| ------------------- | -------------------------------------- |
| `--zone`            | Zone du cluster (ex: `europe-west1-b`) |
| `--region`          | Région si cluster régional             |
| `--project`         | ID du projet                           |
| `--cluster-version` | Version de Kubernetes                  |
| `--release-channel` | Rapid / Regular / Stable               |
| `--async`           | Ne pas attendre la fin de création     |


| Flag                   | Description                                 |
| ---------------------- | ------------------------------------------- |
| `--machine-type`       | Type de machine VM (ex: e2-medium)          |
| `--num-nodes`          | Nombre de nœuds                             |
| `--node-locations`     | Zones supplémentaires (cluster multi-zones) |
| `--disk-size`          | Taille du disque en Go                      |
| `--disk-type`          | pd-standard / pd-balanced / pd-ssd          |
| `--node-taints`        | Ajouter des taints                          |
| `--node-labels`        | Labels sur les nœuds                        |
| `--image-type`         | COS / Ubuntu / Container-Optimized OS       |
| `--enable-autoupgrade` | MAJ auto des nœuds                          |
| `--enable-autorepair`  | Réparation automatique                      |


| Flag                   | Description          |
| ---------------------- | -------------------- |
| `--enable-autoscaling` | Activer l’autoscaler |
| `--min-nodes`          | Minimum de nœuds     |
| `--max-nodes`          | Maximum de nœuds     |

| Flag                                  | Description                         |
| ------------------------------------- | ----------------------------------- |
| `--enable-network-policy`             | Isoler le trafic inter-pods         |
| `--enable-shielded-nodes`             | Renforce la sécurité VM             |
| `--enable-private-nodes`              | Pas d’IP publique sur les nœuds     |
| `--master-ipv4-cidr`                  | CIDR privé pour le master           |
| `--enable-master-authorized-networks` | Limite IP pouvant accéder au master |
| `--master-authorized-networks`        | Liste IP autorisées                 |
| `--service-account`                   | Compte service des nœuds            |
| `--metadata`                          | Ajoute des metadata aux nœuds       |

| Flag                          | Description                 |
| ----------------------------- | --------------------------- |
| `--network`                   | VPC à utiliser              |
| `--subnetwork`                | Sous-réseau                 |
| `--enable-ip-alias`           | Obligatoire pour VPC-Native |
| `--cluster-ipv4-cidr`         | CIDR des pods               |
| `--services-ipv4-cidr`        | CIDR des services           |
| `--default-max-pods-per-node` | Max pods par node           |
| `--enable-load-balancer`      | LB Ingress/Service          |
| `--enable-dataplane-v2`       | Nouveau dataplane optimisé  |

| Flag                        | Description                      |
| --------------------------- | -------------------------------- |
| `--enable-cloud-logging`    | Logs vers Cloud Logging          |
| `--enable-cloud-monitoring` | Monitoring vers Cloud Monitoring |
| `--logging`                 | Choisir quoi logguer             |
| `--monitoring`              | Choisir ce qui est monitoré      |
| `--disable-default-snat`    | Nécessaire pour certains réseaux |

| Flag                         | Description                            |
| ---------------------------- | -------------------------------------- |
| `--workload-pool`            | Activer / configurer Workload Identity |
| `--enable-workload-identity` | Equivalent GKE Autopilot               |

| Flag                        | Description                        |
| --------------------------- | ---------------------------------- |
| `--addons`                  | DNS, Ingress, HPA, Dashboard, etc. |
| `--labels`                  | Labels sur le cluster              |
| `--max-surge-upgrade`       | Nœuds créés pour upgrade           |
| `--max-unavailable-upgrade` | Nœuds en maintenance               |
