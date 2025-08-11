# End-to-End-DevSecOps-Pipeline-with-CI-CD

## Introduction

At every phase of the software development lifecycle (SDLC), advanced security needs to be implemented through continuous integration and continuous delivery (CI/CD) pipelines to ensure that the risk of releasing code with vulnerabilities is detected and minimised early before production rather than leaving it at the end where the issues are more diffciult and costly to resolve. 

The most common tactic attackers use to access an organisation's data and assets is exploiting software vulnerabilities. As a consequence of this, steps taken to fix the breaches are costly and time-consuming, affecting the company's reputation in the process. This is why implementing an end-to-end DevSecOps pipeline with CI/CD is important because it minimises the risk of deploying software with vulnerabilities and misconfigured infrastructure that attackers may exploit. 

This project highlights the integration of the end-to-end DevSecOps pipeline that automates frequent security checks, infrastructure provisioning, application deployment, and enforces security by design at every stage of the SDLC.

### Objectives
1. Utilise GitHub Actions to automate the build, test, scan, and deployment of a containerised application.
2. Integrate security tools early in the pipeline, such as Trivy (vulnerability scanning) and Bandit (static analysis). 
3. Provision infrastructure on Google Cloud Platform (GCP) using Terraform.
4. Use Docker to build and securely package the app with minimal, hardened images.
5. Enable continuous deployment on Google Cloud Run or GKE.
6. Showcase practical DevOps, DevSecOps, and cloud security skills.

## Prequisites

1. Create a <a href="https://cloud.google.com/"> Google Cloud Platform </a> account.
2. <a href="https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli"> Install Terraform </a>:
   - To check if Terraform is installed, run the following command:
      `terraform -help`
    - Initialise Terraform using the following command:
      `terraform init`
      ![image](https://github.com/user-attachments/assets/7cf5ffc3-e110-4941-a7ad-2f703e4bb4c9)
3. Install Windows Subsystem for Linux (WSL) using the following command:
   ```
   wsl --install
   ```
4. <a href="https://cloud.google.com/sdk/docs/install"> Install Google Cloud CLI </a>

## Deployment Stages

### Create a Google Cloud Project

- Once you have created a Google Cloud account, in the top left corner, click "Select a project" and then "New project".
- Name the project "DevSecOps-Pipeline" and click "Create". This will create the new project.
- Head over to the project and note the project ID. This will be relevant when you provision infrastructure to GCP using Terraform.
- Go to "APIs & Services" and enable the following APIs:
  - Cloud Run Admin API
  - Artifact Registry API
  - Cloud Resource Manager
  - Identity and Access Management (IAM) API
  - Compute Engine API
  - Cloud SQL API
  - Cloud SQL Admin API
  - Secret Manager API

### Clone The GitHub Repository

- Before cloning this GitHub repository, download GitHub Desktop on your local machine.
- Once downloaded, go to this GitHub repository on your web browser.
- Once you are on this page, click "Code" in the top right corner and click "Open with GitHub Desktop".
- This will open the desktop application, where you will be prompted to clone this repository and save it in a directory of your choice.
- Once you have selected the directory where you want to save the repository to, click "Clone".
- Ensure the external editor for this GitHub repo is Visual Studio Code. If it isn't, you can change the editor in "Options".
- Open the repo in Visual Studio Code.

### Provision Infrastructure To GCP With Terraform

Once you are in Visual Studio Code with this GitHub repo open, head over to the Terminal and log in to WSL using the following command:

```
wsl -d Ubuntu
```

Log in to Google Cloud CLI using the following command:
```
gcloud init
```

You will be asked to select the account you want to log in to, which is used for the GCP. Once you are logged in, select the Google Cloud project that was created earlier. Next, you will be prompted to configure the compute region and zone to a location of your choice. You can select your preferred location.

Next, use `gcloud` CLI to set up your Application Default Credentials so that Terraform can authenticate to Google Cloud to create infrastructure. Use the following command:
```
gcloud auth application-default login
```

Next, go to the GCP portal in your web browser, then to "IAM and admin", and then to "Service accounts". Click "Create service account" and add the following information:
- Name: terraform-deployer
- Description: Used by Terraform to manage resources
- Assign the following roles to this service account:
  - Editor
  - Viewer
  - Artifact Registry Administrator
  - Cloud Run Admin
  - Compute Storage Admin

Once this service account is created, go to the "Keys" tab for this service account and create a new key in JSON format. Save the key file somewhere safe and do not commit this to this GitHub repo.  

Head over to the WSL terminal and ensure that you are in the directory for this GitHub repo in this terminal. Once you are in this directory, change the directory to the `terraform` directory using the following command:
```
cd terraform
```

Once you are in this directory, initialise Terraform using the following command:
```
terraform init
```

Copy the JSON key file that was generated earlier into the WSL using the following command:
```
cp /mnt/path/to/gcp-key.json ~/gcp-key.json
```
Replace the `gcp-key` with the name of your JSON key file.

Use this key for Terraform and activate it using the following commands:
```
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/gcp-key.json"
gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
```

This will allow Terraform to authenticate to GCP using this key.

Once Terraform is initialised and authenticated to GCP, open the `main.tf` file in the GitHub repo. Provision the following resources:
- Artifact Registry
- Cloud Run

The `main.tf` file should look something like this:
```
terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "6.39.0"
    }
  }
}


provider "google" {
  project     = <Google Project ID>
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
```

The `variables.tf` file should look something like this:
```
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
```

And the `outputs.tf` file should look something like this:
```
output "cloud_run_url" {
  description = "URL of deployed Cloud Run app"
  value       = google_cloud_run_v2_service.app.uri
}
```

Once the resources have been defined in Terraform, you can create an execution plan and apply the proposed changes using the following command:
```
terraform plan
terraform apply
```

This will create a link for the Cloud Run Service:

![image](https://github.com/user-attachments/assets/3162b5d4-40ef-4b4b-b4c9-07d40e31882b)

When you access this link, it gives you an error message:

![image](https://github.com/user-attachments/assets/1e3c674c-862a-4cea-bcde-10c05f55d7f6)

This is because the cloud run is not accessible to the public yet. To enable public access, the Cloud Run Service IAM member needs to be provisioned using Terraform. Add the following to the `main.tf` file:
```
resource "google_cloud_run_v2_service_iam_member" "public_invoker" {
  project = google_cloud_run_v2_service.app.project
  location = google_cloud_run_v2_service.app.location
  name = google_cloud_run_v2_service.app.name
  role = "roles/run.invoker"
  member = "allUsers"
}
```

Then run the following commands:
```
terraform plan
terraform apply
```

This will grant public access to the Cloud Run Service URL. To verify this, visit the link again:

![image](https://github.com/user-attachments/assets/a4da628e-e5ca-4466-a500-9ab32efb0825)

As shown above, the public access to the Cloud Run Service is working, although further deployments to the service will be need to be made to update this page. 

To verify that the Cloud Run Service resource has been successfully provisioned, on the GCP portal, go to the Cloud Run page, and you will see the created service as defined by Terraform:

![image](https://github.com/user-attachments/assets/85305517-a72b-469f-8cbe-f2a404b7b8e6)

For the Artifact Registry Repository resource, go to Artifact Registry, and you will see the repository that was provisioned with Terraform:

![image](https://github.com/user-attachments/assets/da8caec7-1623-498a-be72-df8277f022b4)

Now that the resources have been provisioned, the next steps will be to provision a Cloud SQL instance and database, build an application, containerise it with Docker, push the Docker image to Artifact Registry, and deploy it to Cloud Run. 

### Provisioning Cloud SQL and Secret Manager With Terraform

Before building an application, the MySQL instance, database, and Secret Manager need to be implemented so that the Flask application can connect to them. The Secret Manager is where the environmental variables, such as instance connection name, username, password, and database name, will be safely and securely stored so that when the Flask application runs, it can use these variables to connect to the MySQL instance. In the WSL terminal, change the directory to the `terraform` directory. Once you are in this directory, initialise Terraform using the following command:
```
terraform init
```

Next, authenticate Terraform to GCP using the following command:
```
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/gcp-key.json"
gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
```
Replace the `gcp-key` with the name of your JSON key file.

Open the `main.tf` file in Visual Studio Code and add the following resources:
```
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
```

Terraform will provision the MySQL instance, its database, credentials, and Secret Manager and their secret versions, on the Google Cloud Platform. The `google_secret_manager_secret_version` resource blocks are where you store the contents of each secret, such as the MySQL credentials, connection name, and database name under `secret_data`. When assigning the value for each secret, always use dynamic values, for example `google_sql_user.users.password`, or Terraform variables instead of hardcoded values to ensure the security of the sensitive contents and to allow scalability, as the values may be subject to change. 


In the `variables.tf` file, add the MySQL username as the variable:
```
variable "mysql_username" {
    description = "MySQL username"
    type        = string
    default     = "admin"
}
```

Next, create an execution plan and then apply the changes using the following commands:
```
terraform plan
terraform apply
```

To verify that the resources have been created, on the GCP portal, go to Cloud SQL. You will see that the MySQL instance has been created:

![image](https://github.com/user-attachments/assets/f9e337ee-64d3-4a9e-8139-3b8e0416fe93)

Go to this instance and you can see that the database and user credentials have successfully been created.

![image](https://github.com/user-attachments/assets/21ee7cec-4364-40bc-bb9d-3b4bade0deee)

![image](https://github.com/user-attachments/assets/9848fbe9-a7de-455e-8435-8d1affbcdc16)


Go to Secret Manager. You can see that the secrets have successfully been created by Terraform:

![image](https://github.com/user-attachments/assets/82beee44-3a79-49a1-a276-3f45131a00a1)

If you want to view the secret value, such as the database password, click the secret to which the password is assigned to. Select "Actions" for the latest secret version and click "View secret value". This will show you the secret value, which in this case is the database password.


Next, go to Cloud Run and then to the Cloud Run service that was created earlier. Go to "Edit and deploy new revision" and scroll down to "Cloud SQL connections". Click "Add connection" and select the instance connection name for the MySQL instance that was created earlier, and then select "Deploy":

![image](https://github.com/user-attachments/assets/aa6161b1-357c-4fae-bd77-50cfd05cda32)

### Create A Flask Application

This step involves creating a Flask application before containerising it with Docker. The Flask application is a simple to-do list app that allows the user to create tasks, and when the task is complete, the user clicks the "Mark As Complete" button, and this will move the task to the "Completed Items" section while the pending tasks remain in the "Incomplete Items" section.

The Flask application (`app.py`) uses the `index.html` file as its template.

The directory for the Flask application should look like this:
```
app/
|-- static/
|   |-- style.css
|-- templates/
|   |-- index.html
|-- app.py
|-- requirements.txt
```
Ensure that the `requirements.txt` file contains the following packages along with their latest versions:
- Flask
- Werkzeug
- Cloud SQL Python Connector
- Google Cloud Secret Manager
- SQLAlchemy
- Gunicorn

These are the packages that are required for the Flask application to function. 

Before running the application on your local machine, on the WSL terminal, create the virtual environment and activate it using the following commands:
```
python3 -m venv .venv
source .venv/bin/activate
```

Ensure that the WSL terminal shows that you are in the main directory for this GitHub repository.

On the WSL terminal, change the directory to the `app` directory. Export the environmental variables for the MySQL instance, such as its credentials, using the following command:
```
export GOOGLE_APPLICATION_CREDENTIALS='/path/to/service/account/key.json'
export INSTANCE_CONNECTION_NAME='<PROJECT_ID>:<INSTANCE_REGION>:<INSTANCE_NAME>'
export DB_USER='<YOUR_DB_USER_NAME>'
export DB_PASS='<YOUR_DB_PASSWORD>'
export DB_NAME='<YOUR_DB_NAME>'
```

Note: When the application is deployed to Cloud Run, it will use the latest version of the credentials stored in the Secret Manager.

Once these variables have been exported, run the application using the following command:
```
python3 app.py
```

This is what the web application looks like:

<img width="1919" height="689" alt="image" src="https://github.com/user-attachments/assets/412be365-813d-43ce-90bb-b3afa7f4f252" />

This shows that the to-do list Flask application is successfully working.

### Containerise The Flask Application With Docker

Create a Dockerfile in the `app` directory if you haven't done so already. Ensure the file has no extensions. 

The contents of the Dockerfile should look something like this:
```
FROM python:3.12

# Install the application dependencies
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the remaining source code
COPY . ./

# Expose the port your app will be on
EXPOSE 8000

# Run the application
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]
```

Next, create a service account for the Artifact Registry on Terraform so that it can be used to authenticate Docker with the Artifact Registry. To do this, open the `main.tf` file in the `terraform` directory and add the following resources:
```
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
```

Next, initialise Terraform and apply the changes using the following command:
```
terraform init
terraform plan
terraform apply
```

To verify that the service account for the Artifact Registry has been created, go to "Service accounts" in the GCP portal, and you can see that the service account has been successfully created:

<img width="809" height="492" alt="image" src="https://github.com/user-attachments/assets/d37c3aa8-244b-48ba-9cf3-dbb8f76c35f1" />

Create a key file for this service account so that it can be used for activation.

Next, on the WSL terminal, authenticate Docker to Artifact Registry using the following commands:
```
gcloud auth login
gcloud auth activate-service-account <Artifact-Registry-Service-Account> --key-file="path/to/ArtifactRegistry.json"
```

Replace `path/to/ArtifactRegistry.json` with the actual file path and name of the key file. This will activate the service account. 

Add the repository hostname to the Docker credential helper configuration using the following command:
```
gcloud auth configure-docker <region>-docker.pkg.dev
```
If you want to add more than one region, you can add a comma, for example:
```
gcloud auth configure-docker us-west1-docker.pkg.dev,asia-northeast1-docker.pkg.dev
```
This will update the Docker configuration file:

<img width="1304" height="202" alt="image" src="https://github.com/user-attachments/assets/890a8a9b-e036-4d58-84ce-5c2da0d91279" />

On the WSL terminal, change the directory to the `app` directory using the following commands:
```
cd ..
cd app
```

Add the user that you use to run Docker commands to the Docker security group using the following command:
```
sudo usermod -a -G docker ${USER}
```

To build the container image using the Dockerfile that was created earlier, run the following command:
```
docker build -t LOCATION-docker.pkg.dev/PROJECT_ID/REPOSITORY/IMAGE_NAME:latest .
```

- `LOCATION`: the regional or multi-regional location for your repository.
- `PROJECT_ID`: your Google Cloud project ID.
- `REPOSITORY`: the name of your Artifact Registry repository.
- `IMAGE_NAME`: the name of your container image.

For example:
```
docker build -t europe-west2-docker.pkg.dev/devsecops-pipeline-463112/app-repo/todo_app:latest .
```

This will build the Docker image:

<img width="1677" height="602" alt="image" src="https://github.com/user-attachments/assets/4b7f8323-eb1d-41ad-a771-eddaee8ae40f" />

Next, push the Docker image to the Artifact Registry using the following command:
```
docker push LOCATION-docker.pkg.dev/PROJECT_ID/REPOSITORY/IMAGE_NAME:latest
```

For example:
```
docker push europe-west2-docker.pkg.dev/devsecops-pipeline-463112/app-repo/todo_app:latest
```

<img width="1556" height="225" alt="image" src="https://github.com/user-attachments/assets/bee07202-d861-4f8f-a70d-8944a0def068" />


To verify that the image has been successfully pushed to the Artifact Registry, go to the GCP portal, then to the "Artifact Registry" page, and then to `app-repo` repository page where you will see that the image has successfully been built and pushed along with the latest digest:

<img width="1433" height="354" alt="image" src="https://github.com/user-attachments/assets/05e47653-3c27-4f6e-ac9a-72032681624c" />

The next step will be to update this image under the Cloud Run resource in Terraform so that the Cloud Run can use this image. Additionally, you will also need to integrate the environmental variables for the MySQL credentials, which are stored in the Secret Manager, into the Cloud Run resource block so that Cloud Run can use them to connect to the Cloud SQL instance. The service account for Cloud Run will also need to be created so that it has the necessary permissions to access each of the secrets in the Secret Manager and use them to connect to the Cloud SQL instance.  To do this, open the `main.tf` file and update the following configurations:
```
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
```

The required permissions for the Cloud Run service account should be `roles/cloudsql.client` and `roles/secretmanager.secretAccessor`. The `cloudsql.client` permission allows connectivity to the Cloud SQL instance, while the `secretmanager.secretAccessor` permission allows the service account to read the Secret Manager secrets. The `locals` and `google_secret_manager_secret_iam_member` resource blocks were also created to ensure that the Cloud Run service account has been granted `roles/secretmanager.secretAccessor` on each secret to ensure they are read at runtime. Without these permissions, the Cloud Run will fail during deployment or initialisation because it won't be able to retrieve the required environmental variables used for Cloud SQL connectivity. This will also cause the Cloud Run service to be unavailable as a result.

Apply the changes using the following commands:
```
terraform init
terraform plan
terraform apply
```

This will update the Cloud Run resource block with the image and environmental variables, and create a Cloud Run service account along with its required permissions.

Now, upon accessing the Cloud Run URL, the Flask application is successfully running:

<img width="1919" height="700" alt="image" src="https://github.com/user-attachments/assets/1d068801-9862-4ba5-8719-c3d87683b443" />

https://github.com/user-attachments/assets/58434e8d-1431-4599-9270-6a0bb43e1463

### Build A CI/CD Pipeline Using GitHub Actions

Now that the Flask application is build, containerised using Docker, pushed to the Artifact Registry, and deployed to Cloud Run, where the application is successfully working, the next step is to automate the deployment with CI/CD pipelines using GitHub Action. The purpose of this step is to ensure the software delivery process is fast, reliable, and secure by automatically building, testing, scanning, and deploying your code whenever changes are pushed to your repository. This saves a lot of time on manual deployment and reduces human error. 

Before creating the workflow, the service account for GitHub Actions needs to be created on Terraform so that it can be used to authenticate GitHub Actions with GCP. The following roles need to be granted for the GitHub Actions service account to push/pull to Artifact Registry, access secrets from Secret Manager, connect to Cloud SQL, and deploy to Cloud Run:
- `roles/artifactregistry.reader`
- `roles/artifactregistry.writer`
- `roles/cloudsql.client`
- `roles/secretmanager.secretAccessor`
- `roles/run.admin`
- `roles/iam.serviceAccountUser`

Open the `main.tf` file and add the following configurations:
```
resource "google_service_account" "github_actions_deployer" {
  account_id   = "github-actions-deployer"
  display_name = "GitHub Actions CI/CD Deployer Service Account"
}

resource "google_project_iam_member" "github_actions_deployer" {
  project  = "devsecops-pipeline-463112"
  member   = format("serviceAccount:%s", google_service_account.github_actions_deployer.email)
  for_each = toset([
    "roles/artifactregistry.reader",
    "roles/artifactregistry.writer",
    "roles/cloudsql.client",
    "roles/secretmanager.secretAccessor",
    "roles/run.admin",
    "roles/iam.serviceAccountUser",
  ])
  role     = each.key
}

resource "google_secret_manager_secret_iam_member" "github_actions_secret_access" {
  for_each = local.secrets
  secret_id = each.value
  role = "roles/secretmanager.secretAccessor"
  member = format("serviceAccount:%s", google_service_account.github_actions_deployer.email)
}
```

Apply the changes.

Next, create the service account key for the GitHub Actions using the following command:
```
gcloud iam service-accounts keys create KEY_FILE \
    --iam-account=SA_NAME@PROJECT_ID.iam.gserviceaccount.com
```

For example:
```
gcloud iam service-accounts keys create keyfile.json \
    --iam-account=github-actions-deployer@devsecops-pipeline-463112.iam.gserviceaccount.com
```

Replace the `keyfile.json` with the actual name that you want to give to the key file, and ensure that you are in the directory where you want the key file to be saved on the WSL terminal. You can name your key file `GitHub_GCP_SA_Key.json`.

Once the key file has been created, open it and copy the contents.

Next, on this GitHub repository, go to "Settings", then to "Secrets and variables", and then to "Actions". Click "New repository secret" and paste the contents of the key file into the "Secret" box. Name the repository secret "GCP_CREDENTIALS". Click "Add secret". 

Note: Never commit the JSON key file for the service account to the main branch of this repository due to security reasons. The best practice is to securely store the contents of the JSON key file using GitHub Secrets to encrypt it. 

Create a file called `ci-cd.yml` in the `.github/workflow` directory. Add the jobs in this file that involve authenticating GitHub Actions to GCP, building the Docker image, pushing the image to Artifact Registry, and deploying the image to Cloud Run. 

Commit the changes. If you are editing the file on your local machine, you can push the changes to this GitHub repository. This will automatically start the workflow:

<img width="1919" height="805" alt="image" src="https://github.com/user-attachments/assets/c3e20b6a-5226-4691-9df5-fb22ddc4f8e5" />

The screenshot above shows a successful workflow run. This automated deployment took 1 minute 19 seconds. The manual deployment time, before building this CI/CD pipeline, took 9 minutes 3 seconds. 

### Test The CI/CD Pipeline By Making Changes To The Code 

Now let's change the appearance of the To-Do List web application. Here is the original version:

<img width="1919" height="856" alt="image" src="https://github.com/user-attachments/assets/1b9ef1ed-dff9-467c-a52f-fe23aa567e8f" />

Upon making the changes in appearance and pushing the changes in the code to this repository, this automatically started the workflow, and the deployment to Cloud Run has been successful, as shown below:

<img width="1911" height="798" alt="image" src="https://github.com/user-attachments/assets/25bc29e4-3684-43cb-a39c-9371fb27c086" />

Here is the new appearance of the To-List application:

<img width="1889" height="706" alt="image" src="https://github.com/user-attachments/assets/d3b13dd2-1892-41cc-8079-dbf6dc7a4b66" />

Here are more changes I made to the `index.html` and `style.css` codes that were pushed to this repository, and seamlessly deployed to Cloud Run:

<img width="1280" height="229" alt="image" src="https://github.com/user-attachments/assets/106b959a-2890-41a2-872b-4f99f8e69ff1" />

<img width="1902" height="573" alt="image" src="https://github.com/user-attachments/assets/ed3cf4cb-d6fa-4f75-af35-cd24dddaf38f" />

<img width="1919" height="679" alt="image" src="https://github.com/user-attachments/assets/def82403-9f2b-4fb5-b613-e14876d56d3e" />

This shows that the automated deployment to Cloud Run is successfully working, upon changes made to the code.

### Implement Security Scanning To The CI/CD Pipeline

This step involves implementing scanning tools such as Bandit and Trivy into the CI/CD workflow.

Bandit is designed to find common security issues in the Python code by processing each file, building an abstract syntax tree (AST) from it, and running appropriate plugins against the AST nodes. It would then generate a report after Bandit finishes scanning the files.

Trivy is an open-source vulnerability scanner that is designed to identify security risks, misconfigurations, exposed secrets, and licensing issues in containers, software packages, and file systems, before production. Trivy will be used to scan the Docker image before it is pushed to the Artifact Registry. 

The integration of Bandit and Trivy into the CI/CD pipeline ensures that there is continuous automated detection of code and container vulnerabilities, preventing costly insecure deployments.

In the `ci-cd.yml` YAML file, add the following snippets that set up and run both Bandit and Trivy:
```
- name: Set up Python for Bandit
  uses: actions/setup-python@v5
  with:
    python-version: '3.12'

- name: Install Bandit
  run: |
    pip install bandit

- name: Run Bandit - Python Static Code Analysis
  run: |
    bandit -r ./app --severity-level medium --exit-zero
```
```
- name: Manual Trivy Setup
  uses: aquasecurity/setup-trivy@v0.2.0
  with:
    cache: true
    version: v0.64.1

- name: Run Trivy vulnerability scanner
  uses: aquasecurity/trivy-action@master
  with:
    scan-type: 'image'
    image-ref: ${{env.REGION}}-docker.pkg.dev/${{env.PROJECT_ID}}/${{env.REPO_NAME}}/${{env.IMAGE_NAME}}:latest
    ignore-unfixed: true
    format: 'sarif'
    output: 'trivy-results.sarif'
    severity: 'CRITICAL, HIGH'
    exit-code: '1'
    skip-setup-trivy: true
```

The `--severity-level medium --exit-zero` line ensures that Bandit will not fail the pipeline if the level of vulnerabilities that are medium or below are found. However, if a high or critical level vulnerability is discovered, then Bandit and Trivy will fail the pipeline before the code/image is deployed. 

The `skip-setup-trivy: true` line ensures that Trivy won't repeatedly be set up every time the pipeline is running.

Save the file and push the changes to this repository. This will then start the workflow:

<img width="1903" height="879" alt="image" src="https://github.com/user-attachments/assets/7bc7a020-b0fe-499f-a282-8e7c9c13b728" />

As shown above, the deployment took a bit longer because of the set-up of both Bandit and Trivy. The workflow run above indicates that the Python code and Docker image were able to pass through the Bandit and Trivy scanning before getting deployed to Cloud Run.

If I remove the `--severity-level medium --exit-zero` line, Bandit will now fail the pipeline even if the vulnerabilities discovered are medium-level or below. For example:

<img width="1898" height="858" alt="image" src="https://github.com/user-attachments/assets/0a16ce75-9e64-43c3-8c72-7e5648e99fc4" />

Here are the test results that detail the issue, level of vulnerability discovered, and CWE ID (Common Weakness Enumeration):

<img width="1242" height="820" alt="image" src="https://github.com/user-attachments/assets/fcbc52ba-5ced-4e7d-b461-fca3dfe322c7" />

The reason why there is a medium-level vulnerability is that the Flask application binds to `0.0.0.0` as shown in `app.py`. This will expose the port to all network interfaces, meaning that when the application is running on a local machine without firewalls and/or proper access controls, it may still be reachable for external sources that are listening on `0.0.0.0` to connect to the application. While this is expected in containerised deployments to Cloud Run because GCP handles the network ingress controls, this is still a security risk in other environments. 

Since the Flask application is already being containerised using Docker, and its image getting deployed to Cloud Run on GCP, the vulnerability is a false positive since the application is not running in a local environment. The best option will be to make changes to the `app.py` file by adding the `nosec` comment alongside the `B104` rule right next to the line that Bandit flagged as a medium-level vulnerability, for example:
```
app.run(host="0.0.0.0", port=port) #nosec B104
```

This will ensure that Bandit skips this specific security issue found in this particular line and allow the pipeline to pass as long as there are no other vulnerabilities discovered in this Python code. If there are other vulnerabilities discovered, Bandit will fail the pipeline.

Save the `app.py` file and push the changes to this repository. This will restart the workflow:

<img width="1891" height="933" alt="image" src="https://github.com/user-attachments/assets/25c40786-bcee-4823-a485-913cc8a5c52c" />

As shown above, the workflow was successful as the Python code and Docker image passed through Bandit and Trivy scanning before deployment to Cloud Run. The test results for Bandit show that there are no medium-level vulnerabilities since the `nosec` comment was added to the specific line in the `app.py` file:

<img width="979" height="641" alt="image" src="https://github.com/user-attachments/assets/64690acc-fa12-4a30-b8de-c609c4b0ed30" />

### Add Unit Tests 

Now that Bandit and Trivy are functioning, the next step involves integrating `pytest` into the workflow to ensure that the Flask application is working properly. If the Flask application is not working properly, `pytest` will fail the CI/CD workflow, preventing the deployment of broken code. 

To integrate `pytest` into the workflow, add the following snippet to the `ci-cd.yml` file:
```
- name: Install Dependencies
  run: |
    pip install -r ./app/requirements.txt

- name: Run pytest
  run: |
    pytest -r ./app
```

Create a subfolder within the `app` directory called `tests`, and in this directory, create a file called `test_app.py` so that `pystest` can find it and run it. Ensure that the `pytest` module is in the `requirements.txt` file.

Push the changes to this repository.

Here are the test results:
<img width="1892" height="926" alt="image" src="https://github.com/user-attachments/assets/6450461c-0859-467e-8d2d-437a3803112e" />

The test results show that the Flask application is working properly since it successfully passed through `pytest` scanning, however, Bandit discovered a low-level vulnerability, therefore it had failed the pipeline as shown below:

<img width="1103" height="816" alt="image" src="https://github.com/user-attachments/assets/86b9d2e7-299f-4fba-ad92-2cba875811b9" />

The Bandit test result shows that the vulnerability came from the `test_app.py` file that was created earlier. This is mainly due to the use of `assert` statements in the test code. Unit tests such as `pytest` rely on `assert` statements since it is used for debugging and testing, however, these tests don't run in production environments, therefore, Bandit flags this issue as a security issue. For the Python code to pass Bandit scanning, the best option would be to add the `#nosec` comment along with the `B101` rule right next to the line that has the `asset` statement in the `test_app.py` file, for example:
```
assert response.status_code == 200 #nosec B101
```

Upon pushing the changes in the code to this repository, the workflow run has been successful: 

<img width="1889" height="919" alt="image" src="https://github.com/user-attachments/assets/b1535a5b-4397-4b43-a0cd-fb1c62ac1615" />

### Add Code Quality And Style Checks

This step involves adding a quality tool like Flake8 into the CI/CD pipeline to perform linting against the code syntax and provide instructions on how to clean it. This prevents syntax errors, bad formatting, typos, and other issues early before deployment. As a result, it saves so much time for developers and for people who review the code. This tool is easy to set up and integrate into the CI/CD pipeline. If the mentioned issues are discovered, Flake8 will fail the pipeline until the code style is clean and the said issues are resolved. 

In the `ci-cd.yml` file, add the following snippet before `pytest`:
```
- name: Run Flake8 Linting
  run: |
    flake8 ./app
```

Flake8 should run before `pytest` so that the code style and syntax issues are discovered and mitigated early, before running further tests with other static code analysis tools like `pytest` and Bandit. Ensure that the Flake8 module is in the `requirements.txt` file in the `app` directory. 

Save the `ci-cd.yml` file and push the changes to this repository. This will start another workflow run:

<img width="1885" height="921" alt="image" src="https://github.com/user-attachments/assets/93f61ad4-7d43-4603-a05a-f97977ee0d74" />

The workflow run shown above illustrates that the code style and syntax issues have been discovered by Flake8, therefore the pipeline failed:

<img width="808" height="854" alt="image" src="https://github.com/user-attachments/assets/db1e507d-dfb9-4b31-abe8-52c2014839b4" />

The results shown above state which areas in the code have issues, such as unused imports, lengthy lines, and spacing, along with instructions on how to clean the format. 

Upon making the suggested changes to ensure that the code style and synatax is clean, the Python code was able to pass quality checks which in turn allowed the code to go through the subsequent static code analysis tests in the pipeline.

## References
- https://squareops.com/ci-cd-security-devsecops/#:~:text=Why%20SquareOps%20is%20the%20Right,security%20for%20your%20software%20delivery.
- https://www.microsoft.com/en-gb/security/business/security-101/what-is-devsecops#:~:text=DevSecOps%2C%20which%20stands%20for%20development,releasing%20code%20with%20security%20vulnerabilities.
- https://cloud.google.com/compute/docs/regions-zones#choosing_a_region_and_zone
- https://jozimarback.medium.com/using-github-actions-with-terraform-on-gcp-d473a37ddbd6
- https://developer.hashicorp.com/terraform/tutorials/gcp-get-started/google-cloud-platform-build
- https://registry.terraform.io/providers/hashicorp/google/latest/docs
- https://cloud.google.com/run/docs/authenticating/public#terraform
- https://developer.hashicorp.com/terraform/tutorials/gcp-get-started/google-cloud-platform-variables
- https://spacelift.io/blog/how-to-use-terraform-variables
- https://www.geeksforgeeks.org/how-to-use-a-dockerignore-file/
- https://cloud.google.com/sql/docs/mysql/create-instance
- https://cloud.google.com/sql/pricing?hl=en#section-1
- https://cloud.google.com/sql/docs/mysql/machine-series-overview
- https://developer.hashicorp.com/terraform/language/resources/ephemeral/write-only
- https://medium.com/terraform-using-google-cloud-platform/terraform-for-gcp-how-to-create-cloud-sql-0a558840914c
- https://cloud.google.com/composer/docs/composer-3/set-environment-variables?_gl=1*13sj2ie*_ga*OTk3ODk5MTE5LjE3NTAwNzU4NDU.*_ga_WH2QY8WWF5*czE3NTEyMjM5OTgkbzExJGcxJHQxNzUxMjI4NTI3JGo2MCRsMCRoMA..#terraform
- https://cloud.google.com/composer/docs/composer-3/terraform-create-environments
- https://cloud.google.com/blog/topics/developers-practitioners/how-connect-cloud-sql-using-python-easy-way
- https://cloud.google.com/sql/docs/mysql/samples/cloud-sql-mysql-sqlalchemy-connect-connector
- https://cloud.google.com/sql/docs/mysql/connect-run
- https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/cloud-sql/mysql/sqlalchemy/README.md
- https://medium.com/@faizififita1/connect-your-python-app-to-google-cloud-sql-the-easy-way-7e459de2f4e9
- https://medium.com/@terwaljoop/just-a-devsecops-project-to-showcase-your-skills-and-knowledge-on-your-cv-and-github-60610005b097
- https://cloud.google.com/secret-manager/docs/creating-and-accessing-secrets#gcloud
- https://cloud.google.com/secret-manager/docs/reference/libraries#client-libraries-install-python
- https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application
- https://cloud.google.com/secret-manager/docs/view-secret-version
- https://cloud.google.com/secret-manager/docs/access-secret-version
- https://docs.sqlalchemy.org/en/14/core/engines.html#escaping-special-characters-such-as-signs-in-passwords
- https://pypi.org/project/cloud-sql-python-connector/
- https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/cloud-sql/mysql/sqlalchemy/app.py
- https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/cloud-sql/mysql/sqlalchemy/connect_connector.py
- https://medium.com/@pythoncodelab/building-a-to-do-list-app-in-python-a-step-by-step-guide-ce34b9ea141a
- https://docs.sqlalchemy.org/en/14/core/engines.html#escaping-special-characters-such-as-signs-in-passwords
- https://www.geeksforgeeks.org/python/todo-list-app-using-flask-python/
- https://colab.research.google.com/github/GoogleCloudPlatform/cloud-sql-python-connector/blob/main/samples/notebooks/postgres_python_connector.ipynb#scrollTo=yjAPpIDdRfu2
- https://medium.com/@faizififita1/connect-your-python-app-to-google-cloud-sql-the-easy-way-7e459de2f4e9
- https://stackoverflow.com/questions/73493052/how-to-connect-to-cloud-sql-using-python
- https://sibabalwesinyaniso.medium.com/connecting-to-a-database-and-creating-tables-using-sqlalchemy-core-52cb79e51ca4
- https://www.w3schools.com/sql/sql_update.asp
- https://docs.sqlalchemy.org/en/20/core/engines.html
- https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table
- https://docs.sqlalchemy.org/en/20/core/dml.html
- https://docs.sqlalchemy.org/en/20/core/connections.html#using-transactions
- https://docs.docker.com/guides/python/develop/
- https://www.geeksforgeeks.org/cloud-computing/what-is-dockerfile/
- https://docs.docker.com/get-started/docker-concepts/building-images/writing-a-dockerfile/
- https://dev.to/prodevopsguytech/writing-a-dockerfile-beginners-to-advanced-31ie
- https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/cloud-sql/mysql/sqlalchemy/Dockerfile
- https://www.w3schools.com/python/python_virtualenv.asp
- https://docs.docker.com/get-started/docker-concepts/building-images/build-tag-and-publish-an-image/#build-an-image
- https://cloud.google.com/artifact-registry/docs/docker/authentication
- https://cloud.google.com/artifact-registry/docs/docker/pushing-and-pulling
- https://medium.com/@prayag-sangode/create-a-docker-gcp-artifactory-registry-c271a467e574
- https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/secret_manager_secret_iam
- https://developer.hashicorp.com/terraform/language/meta-arguments/for_each
- https://cloud.google.com/iam/docs/roles-overview
- https://cloud.google.com/iam/docs/keys-create-delete#iam-service-account-keys-create-gcloud
- https://medium.com/@pathirage/step-in-to-ci-cd-a-hands-on-guide-to-building-ci-cd-pipeline-with-github-actions-7490d6f7d8ff
- https://docs.github.com/en/actions/tutorials/build-and-test-code/python
- https://cloud.google.com/blog/products/devops-sre/using-github-actions-with-google-cloud-deploy
- https://cloud.google.com/blog/products/devops-sre/deploy-to-cloud-run-with-github-actions/
- https://medium.com/google-cloud/create-a-ci-cd-pipeline-using-github-actions-and-google-cloud-9be20ff50e97
- https://faun.pub/publishing-your-image-to-google-cloud-artifact-8ba7675ca594
- https://discuss.google.dev/t/permission-artifactregistry-repositories-uploadartifacts-denied-on-resource-projects-xxx/107225/2
- https://github.com/pulumi/pulumi-cloud-requests/issues/349
- https://trivy.dev/v0.53/ecosystem/cicd/
- https://medium.com/%40fanjum524/office-hours-integrating-trivy-in-github-actions-ci-for-end-to-end-repository-security-devsecops-e7aa640eca51
- https://github.com/PyCQA/bandit-action/tree/main
- https://bandit.readthedocs.io/en/latest/ci-cd/github-actions.html
- https://www.jit.io/resources/appsec-tools/when-and-how-to-use-trivy-to-scan-containers-for-vulnerabilities
- https://dev.to/luzkalidgm/how-to-use-bandit-as-a-sast-tool-for-your-python-app-1b0e
- https://github.com/aquasecurity/trivy-action
- https://bandit.readthedocs.io/en/latest/plugins/b104_hardcoded_bind_all_interfaces.html
- https://cwe.mitre.org/data/definitions/605.html
- https://nvd.nist.gov/vuln/detail/CVE-2018-1281
- https://calmcode.io/course/bandit/nosec
- https://naodeng.medium.com/pytest-tutorial-advance-usage-integration-ci-cd-and-github-action-c627c7cbbc22
- https://cwe.mitre.org/data/definitions/703.html
- https://realpython.com/pytest-python-testing/
- https://flake8.pycqa.org/en/latest/
- https://medium.com/python-pandemonium/what-is-flake8-and-why-we-should-use-it-b89bd78073f2
