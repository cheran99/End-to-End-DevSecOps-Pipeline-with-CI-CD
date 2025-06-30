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

resource "google_service_account" "composer_sa" {
  account_id   = "composer-sa"
  display_name = "Cloud Composer Service Account"
}

resource "google_project_iam_member" "composer_sa" {
  project  = "devsecops-pipeline-463112"
  member   = format("serviceAccount:%s", google_service_account.composer_sa.email)
  role     = "roles/composer.worker"
}

resource "google_composer_environment" "devsecops_env" {
  name = "devsecops-env"

  config {

    software_config {
      image_version = "composer-3-airflow-2.10.5-build.7"
      env_variables = {
        DB_USER     = google_sql_user.users.name
        DB_PASS     = google_sql_user.users.password
        DB_NAME     = google_sql_database.devsecops_db.name
      }
    }

    node_config {
      service_account = google_service_account.composer_sa.email
    }

  }
}