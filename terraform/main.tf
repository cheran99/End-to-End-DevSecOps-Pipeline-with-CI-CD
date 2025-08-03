terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "6.39.0"
    }
  }
}


provider "google" {
  project     = "devsecops-pipeline-463112"
  region      = var.region
  zone        = var.zone
}

resource "google_artifact_registry_repository" "docker_repo" {
  location      = var.region
  repository_id = "app-repo"
  description   = "Docker repo for CI/CD"
  format        = "DOCKER"
}

resource "google_service_account" "artifactregistry_sa" {
  account_id   = "artifactregistry-sa"
  display_name = "Artifact Registry Service Account"
}

resource "google_project_iam_member" "artifactregistry_sa" {
  project  = "devsecops-pipeline-463112"
  member   = format("serviceAccount:%s", google_service_account.artifactregistry_sa.email)
  for_each = toset([
    "roles/artifactregistry.reader",
    "roles/artifactregistry.writer",
  ])
  role     = each.key
}

resource "google_cloud_run_v2_service" "app" {
  name     = "devsecops-app"
  location = var.region
  deletion_protection = false
  ingress = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = "europe-west2-docker.pkg.dev/devsecops-pipeline-463112/app-repo/todo_app:latest"
      ports {
        container_port = 8000
      }

      env {
        name = "INSTANCE_CONNECTION_NAME"
        value_source {
          secret_key_ref {
            secret = google_secret_manager_secret.instance_conn.id
            version = "latest"
          }
        }
      }

      env {
        name = "DB_USER"
        value_source {
          secret_key_ref {
            secret = google_secret_manager_secret.db_user.id
            version = "latest"
          }
        }
      }

      env {
        name = "DB_PASS"
        value_source {
          secret_key_ref {
            secret = google_secret_manager_secret.db_pass.id
            version = "latest"
          }
        }
      }

      env {
        name = "DB_NAME"
        value_source {
          secret_key_ref {
            secret = google_secret_manager_secret.db_name.id
            version = "latest"
          }
        }
      }
    }

    service_account = google_service_account.cloudrun_sa.email
  }

  depends_on = [google_sql_database_instance.mysql_devsecops]
}

resource "google_service_account" "cloudrun_sa" {
  account_id   = "cloudrun-sa"
  display_name = "Cloud Run Service Account"
}

resource "google_project_iam_member" "cloudrun_sa" {
  project  = "devsecops-pipeline-463112"
  member   = format("serviceAccount:%s", google_service_account.cloudrun_sa.email)
  for_each = toset([
    "roles/cloudsql.client",
    "roles/secretmanager.secretAccessor",
  ])
  role     = each.key
}

resource "google_cloud_run_v2_service_iam_member" "public_invoker" {
  project = google_cloud_run_v2_service.app.project
  location = google_cloud_run_v2_service.app.location
  name = google_cloud_run_v2_service.app.name
  role = "roles/run.invoker"
  member = "allUsers"
}

resource "google_sql_database_instance" "mysql_devsecops" {
  name             = "mysql-devsecops"
  region           = var.region
  database_version = "MYSQL_8_0"
  settings {
    tier           = "db-g1-small" 
  }

  deletion_protection  = true
}

resource "google_sql_database" "devsecops_db" {
  name             = "devsecopsdb"
  instance         = google_sql_database_instance.mysql_devsecops.name
}

resource "random_password" "password" {
  length           = 16
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

resource "google_sql_user" "users" {
  name             = var.mysql_username
  instance         = google_sql_database_instance.mysql_devsecops.name
  password         = random_password.password.result
}

resource "google_service_account" "secretmanager_sa" {
  account_id   = "secretmanager-sa"
  display_name = "Secret Manager Service Account"
}

resource "google_project_iam_member" "secretmanager_sa" {
  project  = "devsecops-pipeline-463112"
  member   = format("serviceAccount:%s", google_service_account.secretmanager_sa.email)
  role     = "roles/secretmanager.admin"
}

resource "google_secret_manager_secret" "instance_conn" {
  secret_id = "instance-connection-name"
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "instance_conn_version" {
  secret = google_secret_manager_secret.instance_conn.id
  secret_data = "devsecops-pipeline-463112:europe-west2:mysql-devsecops"
}

resource "google_secret_manager_secret" "db_user" {
  secret_id = "db-user"
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "db_user_version" {
  secret = google_secret_manager_secret.db_user.id
  secret_data = var.mysql_username
}

resource "google_secret_manager_secret" "db_pass" {
  secret_id = "db-pass"
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "db_pass_version" {
  secret = google_secret_manager_secret.db_pass.id
  secret_data = google_sql_user.users.password
}

resource "google_secret_manager_secret" "db_name" {
  secret_id = "db-name"
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "db_name_version" {
  secret = google_secret_manager_secret.db_name.id
  secret_data = google_sql_database.devsecops_db.name
}

locals {
  secrets = {
    instance_conn = google_secret_manager_secret.instance_conn.id,
    db_user       = google_secret_manager_secret.db_user.id,
    db_name       = google_secret_manager_secret.db_name.id,
    db_pass       = google_secret_manager_secret.db_pass.id,
  }
}

resource "google_secret_manager_secret_iam_member" "cloudrun_secret_access" {
  for_each = local.secrets
  secret_id = each.value
  role = "roles/secretmanager.secretAccessor"
  member = format("serviceAccount:%s", google_service_account.cloudrun_sa.email)
}