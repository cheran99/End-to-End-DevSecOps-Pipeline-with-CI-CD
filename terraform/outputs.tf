output "cloud_run_url" {
  description = "URL of deployed Cloud Run app"
  value       = google_cloud_run_service.app.status[0].url
}