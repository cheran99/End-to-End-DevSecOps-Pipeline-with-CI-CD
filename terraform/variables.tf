variable "region" {
    description = "GCP region"
    type        = string
    default     = "europe-west2"
}

variable "zone" {
    description = "GCP zone"
    type        = string
    default     = "europe-west2-a"
}

variable "mysql_username" {
    description = "MySQL username"
    type        = string
    default     = "admin"
}

variable "mysql_password" {
    description = "MySQL password"
    type        = string
    sensitive   = true
}