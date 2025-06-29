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
  name     = "devsecopsdb"
  instance = google_sql_database_instance.mysql_devsecops.name
}

resource "google_sql_user" "users" {
  name     = var.mysql_username
  instance = google_sql_database_instance.mysql_devsecops.name
  password_wo = var.mysql_password
}