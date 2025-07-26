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
      image = "us-docker.pkg.dev/cloudrun/container/hello"
    }
  }
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