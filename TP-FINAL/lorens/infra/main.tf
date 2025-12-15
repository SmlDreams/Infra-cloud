resource "google_artifact_registry_repository" "vaultaire" {
  location      = var.region
  repository_id = "vaultaire"
  format        = "DOCKER"
}

resource "google_container_cluster" "vaultaire_cluster" {
  name     = "tpfinal-kubcluster"
  location = var.zone

  initial_node_count = 2

  node_config {
    machine_type = "e2-medium"
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}
