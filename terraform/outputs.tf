output "cloud_run_url" {
  description = "URL of deployed Cloud Run app"
  value       = google_cloud_run_v2_service.app.uri
}