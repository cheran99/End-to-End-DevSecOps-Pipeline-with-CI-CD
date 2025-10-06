# End-to-End-DevSecOps-Pipeline-with-CI-CD

## 🧐 Overview

At every phase of the software development lifecycle (SDLC), advanced security needs to be implemented through continuous integration and continuous delivery (CI/CD) pipelines to ensure that the risk of releasing code with vulnerabilities is detected and minimised early before production rather than leaving it at the end where the issues are more diffciult and costly to resolve. 

The most common tactic attackers use to access an organisation's data and assets is exploiting software vulnerabilities. As a consequence of this, steps taken to fix the breaches are costly and time-consuming, affecting the company's reputation in the process. This is why implementing an end-to-end DevSecOps pipeline with CI/CD is important because it minimises the risk of deploying software with vulnerabilities and misconfigured infrastructure that attackers may exploit. 

This project highlights the integration of the end-to-end DevSecOps pipeline that automates frequent security checks, infrastructure provisioning, application deployment, and enforces security by design at every stage of the SDLC.

## 🎯 Objectives
1. Utilise GitHub Actions to automate the build, test, scan, and deployment of a containerised application.
2. Integrate security tools early in the pipeline, such as Trivy (vulnerability scanning) and Bandit (static analysis). 
3. Provision infrastructure on Google Cloud Platform (GCP) using Terraform.
4. Use Docker to build and securely package the app with minimal, hardened images.
5. Enable continuous deployment on Google Cloud Run or GKE.
6. Showcase practical DevOps, DevSecOps, and cloud security skills.

## 📦 Project Structure
```
/
├── .github/
│ └── workflows/ # GitHub Actions workflows (CI/CD pipelines)
├── app/
│ ├── static/
│ ├── templates/
│ ├── tests/ # unit tests/integration tests
│ ├── app.py
│ ├── requirements.txt
│ └── Dockerfile
├── terraform/
│ ├── main.tf
│ ├── variables.tf
│ ├── outputs.tf
│ └── modules/ # (if any)
├── Dashboards/
│ └── ... # for monitoring / logging dashboards, if applicable
├── .dockerignore
├── .gitignore
└── README.md
```

## 🔧 Tech Stack

| Layer | Technologies / Tools |
|-------|-------------------------|
| Infrastructure & Cloud | GCP (Cloud Run, Artifact Registry, Cloud SQL, IAM, Secret Manager) |
| IaC / Provisioning | Terraform |
| Application | Python (Flask), HTML/CSS |
| Containerisation | Docker |
| CI/CD / Automation | GitHub Actions |
| Security / Quality | Bandit, Trivy, Flake8, pytest |
| Monitoring & Logging (Optional / Further Work) | Prometheus, Grafana, Google Cloud Logging |

## ✅ Prerequisites

- A **Google Cloud Platform** account with billing enabled.  
- Installations on your machine (or development environment / WSL):  
    • Terraform  
    • Google Cloud CLI (`gcloud`)  
    • Docker  
    • Python3 + pip + virtualenv  
- Access/permissions to provision GCP services: IAM roles to create/run Cloud Run, Cloud SQL, Secret Manager, Artifact Registry, etc.

## 🚀 Setup & Deployment

1. Create a Google Cloud Project
   -  Name the project "DevSecOps-Pipeline" and click "Create". This will create the new project.
   -  Note the project ID. This will be relevant when you provision infrastructure to GCP using Terraform.
   -  Go to "APIs & Services" and enable the following APIs:
       - Cloud Run Admin API
       - Artifact Registry API
       - Cloud Resource Manager
       - Identity and Access Management (IAM) API
       - Compute Engine API
       - Cloud SQL API
       - Cloud SQL Admin API
       - Secret Manager API

2. Clone The GitHub Repository
   - Go to this GitHub repository on your web browser.
   - Click "Code" in the top right corner and click "Open with GitHub Desktop".
   - This will open the desktop application, where you will be prompted to clone this repository and save it in a directory of your choice.
   - Once you have selected the directory where you want to save the repository, click "Clone".
   - Ensure the external editor for this GitHub repo is Visual Studio Code. If it isn't, you can change the editor in "Options".
   - Open the repo in Visual Studio Code.

3. Provision Infrastructure To GCP With Terraform
   - Once you are in Visual Studio Code with this GitHub repo open, head over to the Terminal and log in to WSL using the following command:
      ```
      wsl -d Ubuntu
      ```
   - Log in to Google Cloud CLI using the following commands:
      ```
      gcloud init
      gcloud auth application-default login
      ```
   - Create a service account to allow GCP to authenticate to Terraform to create and manage resources.
   - Assign the following roles to this service account:
      - Editor
      - Viewer
      - Artifact Registry Administrator
      - Cloud Run Admin
      - Compute Storage Admin
   - Download the key file for this service account and save it in JSON format. Store the key file somewhere safe.
   -  ```
      cd terraform
      ```
   - Activate the key file for the Terraform service account using the following commands:
      ```
      export GOOGLE_APPLICATION_CREDENTIALS="$HOME/gcp-key.json"
      gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
      ```
   - Set up the resources, variables, and outputs in the `main.tf`, `outputs.tf`, and `variables.tf` files.
   - Run:
     ```
     terraform init
     terraform plan
     terraform apply
     ```

4. Create A Flask Application
   - Create and activate a Python virtual environment:
     ```
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - Go to `app` directory:
     ```
     cd app
     ```
   - Install dependencies:
     ```
     pip3 install -r requirements.txt
     ```
   - Export the environmental variables for the MySQL credentials to test run the Flask application:
     ```
      export GOOGLE_APPLICATION_CREDENTIALS='/path/to/service/account/key.json'
      export INSTANCE_CONNECTION_NAME='<PROJECT_ID>:<INSTANCE_REGION>:<INSTANCE_NAME>'
      export DB_USER='<YOUR_DB_USER_NAME>'
      export DB_PASS='<YOUR_DB_PASSWORD>'
      export DB_NAME='<YOUR_DB_NAME>'
     ```
   - Test run the Flask application:
     ```
     python3 app.py
     ```
     <img width="1919" height="689" alt="image" src="https://github.com/user-attachments/assets/412be365-813d-43ce-90bb-b3afa7f4f252" />

5. Containerise The Flask Application With Docker
   - Create a Dockerfile in the `app` directory
   - Create a service account for the Artifact Registry on Terraform and assign the following roles:
     - `roles/artifactregistry.reader`
     - `roles/artifactregistry.writer`
   - Run:
      ```
      terraform init
      terraform plan
      terraform apply
      ```
   - Download the key file for this service account and save it in JSON format.
   - Activate the service account using this key file to authenticate Docker to Artifact Registry:
      ```
      gcloud auth login
      gcloud auth activate-service-account <Artifact-Registry-Service-Account> --key-file="path/to/ArtifactRegistry.json"
      ```
   - Add the repository hostname to the Docker credential helper configuration using the following command:
      ```
      gcloud auth configure-docker <region>-docker.pkg.dev
      ```
      <img width="1304" height="202" alt="image" src="https://github.com/user-attachments/assets/890a8a9b-e036-4d58-84ce-5c2da0d91279" />
   - Add the user that you use to run Docker commands to the Docker security group using the following command:
      ```
      sudo usermod -a -G docker ${USER}
      ```
   - Build the Docker image:
      ```
      docker build -t LOCATION-docker.pkg.dev/PROJECT_ID/REPOSITORY/IMAGE_NAME:latest .
      ```
      - `LOCATION`: the regional or multi-regional location for your repository.
      - `PROJECT_ID`: your Google Cloud project ID.
      - `REPOSITORY`: the name of your Artifact Registry repository.
      - `IMAGE_NAME`: the name of your container image.
    - Push the Docker image to the Artifact Registry:
      ```
      docker push LOCATION-docker.pkg.dev/PROJECT_ID/REPOSITORY/IMAGE_NAME:latest
      ```

6. Deploy container image to Cloud Run
   - Create a Cloud Run service account on Terraform with the following permissions:
     - `roles/cloudsql.client`
     - `roles/secretmanager.secretAccessor`
     - `roles/artifactregistry.reader`
   - Run:
     ```
     terraform init
     terraform plan
     terraform apply
     ```
   - Go to the `app` directory:
     ```
     cd app
     ```
   - Deploy to Cloud Run using the Cloud Run service account:
     ```
     gcloud run deploy SERVICE_NAME \
      --image=LOCATION-docker.pkg.dev/PROJECT_ID/REPOSITORY/IMAGE_NAME:latest \
      --region=LOCATION \
      --service-account=cloudrun-sa@PROJECT_ID.iam.gserviceaccount.com
     ```
     <img width="1919" height="700" alt="image" src="https://github.com/user-attachments/assets/1d068801-9862-4ba5-8719-c3d87683b443" />

     https://github.com/user-attachments/assets/58434e8d-1431-4599-9270-6a0bb43e1463

7. Build a CI/CD pipeline using GitHub Actions to automate deployment to Cloud Run
   - Create a GitHub Actions service account on Terraform with the following permissions:
     - `roles/artifactregistry.reader`
     - `roles/artifactregistry.writer`
     - `roles/cloudsql.client`
     - `roles/secretmanager.secretAccessor`
     - `roles/run.admin`
     - `roles/iam.serviceAccountUser`
   - Create the service account key file for the GitHub Actions:
      ```
      gcloud iam service-accounts keys create GitHub_GCP_SA_Key.json \
          --iam-account=github-actions-deployer@PROJECT_ID.iam.gserviceaccount.com
      ```
   - Copy the contents of the key file and save it to GitHub Secrets. Note: Never commit the JSON key file for the service account to the main branch of this repository due to security reasons. The best practice is to securely store the contents of the JSON key file using GitHub Secrets to encrypt it.
   - Create a file called `ci-cd.yml` in the `.github/workflow` directory. Add the jobs in this file that involve authenticating GitHub Actions to GCP, building the Docker image, pushing the image to Artifact Registry, and deploying the image to Cloud Run.
   - Commit the changes. This will automatically start the workflow:
      <img width="1919" height="805" alt="image" src="https://github.com/user-attachments/assets/c3e20b6a-5226-4691-9df5-fb22ddc4f8e5" />

8. Test The CI/CD Pipeline By Making Changes To The Code
   - Make changes to the Flask application and push it to this repository:
     <img width="1911" height="798" alt="image" src="https://github.com/user-attachments/assets/25bc29e4-3684-43cb-a39c-9371fb27c086" />

     <img width="1889" height="706" alt="image" src="https://github.com/user-attachments/assets/d3b13dd2-1892-41cc-8079-dbf6dc7a4b66" />

     <img width="1902" height="573" alt="image" src="https://github.com/user-attachments/assets/ed3cf4cb-d6fa-4f75-af35-cd24dddaf38f" />

     <img width="1919" height="679" alt="image" src="https://github.com/user-attachments/assets/def82403-9f2b-4fb5-b613-e14876d56d3e" />

9. Implement security scanning into the CI/CD pipeline
    - Add static code analysis (Bandit), vulnerability scanning (Trivy), unit tests (pytest), and linting (Flake8) into the CI/CD workflow.

10. Test the security scanning
    - Remove the `--severity-level medium --exit-zero` line from the `ci-cd.yml` file and run the workflow:

        <img width="1898" height="858" alt="image" src="https://github.com/user-attachments/assets/0a16ce75-9e64-43c3-8c72-7e5648e99fc4" />

        <img width="1242" height="820" alt="image" src="https://github.com/user-attachments/assets/fcbc52ba-5ced-4e7d-b461-fca3dfe322c7" />
      
      - Add the `#nosec` comment alongside rules like `B104` next to the line that Bandit flagged as a false positive for a medium-level vulnerability in the `app.py` file and push the changes to this repository:

          <img width="1891" height="933" alt="image" src="https://github.com/user-attachments/assets/25c40786-bcee-4823-a485-913cc8a5c52c" />

          <img width="979" height="641" alt="image" src="https://github.com/user-attachments/assets/64690acc-fa12-4a30-b8de-c609c4b0ed30" />

    - Run code quality and style checks with Flake8:

        <img width="1885" height="921" alt="image" src="https://github.com/user-attachments/assets/93f61ad4-7d43-4603-a05a-f97977ee0d74" />

        <img width="808" height="854" alt="image" src="https://github.com/user-attachments/assets/db1e507d-dfb9-4b31-abe8-52c2014839b4" />
      
      - Make the suggested changes to the Python code and push it to this repository:
        
        <img width="1896" height="943" alt="image" src="https://github.com/user-attachments/assets/5b0f2164-15fc-4155-9254-6db91d13c953" />

11. Test the CSRF protection
    - Open the Cloud Run URL for the Flask application in your web browser.
    - Press F12 to open the developer tools:

      <img width="1919" height="776" alt="image" src="https://github.com/user-attachments/assets/098562c4-f021-493e-adc1-ec628a1e2c16" />
      
    - Add a new to-do item.
    - Go to the "Network" tab in the developer tools and observe the "add" request:

      <img width="512" height="646" alt="image" src="https://github.com/user-attachments/assets/5bfe01dd-cde0-43c2-8801-4f3c1b1543cd" />
      
    - Go to the "Payload" section to view the generated value for the CSRF token along with the added to-do item:

      <img width="458" height="185" alt="image" src="https://github.com/user-attachments/assets/97dad489-228a-4a3a-9364-f38b4c54a774" />
      
    - Go to the "Elements" section in the developer tools.
    - Find the CSRF token line and replace the token value with a random string:

      <img width="580" height="365" alt="image" src="https://github.com/user-attachments/assets/7aa19075-870a-4cbc-a1a9-df8917a0cd91" />
      
    - Add a new to-do list item:

      <img width="809" height="247" alt="image" src="https://github.com/user-attachments/assets/ae268fa5-5246-4e4d-8f07-951f74c4ba61" />
      
      <img width="536" height="222" alt="image" src="https://github.com/user-attachments/assets/648d2f51-e060-46ea-9c05-df58daaed298" />
      
      <img width="542" height="227" alt="image" src="https://github.com/user-attachments/assets/e19ed319-b92c-4a28-94c7-85e4649dd47e" />



12. Automate the CSRF protection test
    - Create a `test_csrf.py` file in the `app/tests` directory.
    - Add the Python code for `pytest` to run the automated tests in the CI/CD pipeline.
    - Push the changes to the repository:

      <img width="1863" height="710" alt="image" src="https://github.com/user-attachments/assets/76df50b4-bc3f-4f68-aae8-f41394ae60bf" />

13. Test the automated CSRF protection test
    - Change the value for the `app.config['WTF_CSRF_ENABLED']` line in the `test_csrf.py` file from `True` to `False`, and push the changes to this repository:

      <img width="1884" height="907" alt="image" src="https://github.com/user-attachments/assets/177a8858-2312-4c60-bccd-c0319af8e2d4" />
    - Change the value for the `app.config['WTF_CSRF_ENABLED']` back to `True`.
    - Change the test assertion status code from 400 to 200, and push the changes to this repository:

      <img width="1890" height="924" alt="image" src="https://github.com/user-attachments/assets/18e28349-780f-49d5-ae44-9fc4a34c0c83" />
    - Change the expected status code for the test assertion from 200 back to 400 and push the changes to this repository.

14. Implement security best practices in the Docker image
    - Run a Trivy scan through the GitHub Actions workflow run.
    - The scan would fail the security check if HIGH/CRITICAL level vulnerabilities are found:

      <img width="1878" height="921" alt="image" src="https://github.com/user-attachments/assets/d0d12d34-374a-4d2d-9080-7bb78bd72b38" />

      <img width="1314" height="738" alt="image" src="https://github.com/user-attachments/assets/f200a2b8-5607-4233-9fd8-803cacc9912b" />

      <img width="1294" height="857" alt="image" src="https://github.com/user-attachments/assets/a082717f-4477-492a-890d-ef276b777440" />

      <img width="1356" height="883" alt="image" src="https://github.com/user-attachments/assets/2eeb67b7-afcb-4e17-911f-624bad65a586" />

    - To minimise the vulnerabilities, add the following configurations to the Dockerfile to ensure the system packages are consistently up-to-date with the latest patches, whilst removing any unnecessary extra packages:
      ```
      RUN apt-get update && \
          apt-get upgrade -y && \
          apt-get install -y --no-install-recommends \
              gcc \
              libxslt1-dev \
              libxml2-dev \
              build-essential && \
          apt-get clean && rm -rf /var/lib/apt/lists/*
      ```
    - Push the changes to the repository:

      <img width="1897" height="902" alt="image" src="https://github.com/user-attachments/assets/562673c0-7df0-48cd-990c-f43580dcf63e" />

15. Add monitoring and logging
    - Create a `prometheus.yml` file in the `app` directory to scrape log metrics from the Flask application.
    - Create a `docker-compose.yml` file in the `app` directory for Docker to run services like Prometheus and Grafana, and build the Docker image from the Dockerfile in one go.
    - Run the services using the following command:
      ```
      docker compose build
      docker compose up
      ```
    - Visit Prometheus on the web browser: `http://localhost:9090`
      - Add queries for the metrics Prometheus scrapes:
        - Total add requests:

          <img width="1905" height="302" alt="image" src="https://github.com/user-attachments/assets/325c20da-eef5-45b7-b8fb-17470abd047d" />
        - Latency of added requests:

          <img width="1909" height="760" alt="image" src="https://github.com/user-attachments/assets/ce9f9256-59a7-4bcb-bb69-2bf80e305049" />
        - Total number of CSRF failures:

          <img width="1913" height="292" alt="image" src="https://github.com/user-attachments/assets/ea9548f6-3e01-4d16-872f-b673eaebdc6c" />

    - To visualise the logs, visit Grafana: `http://localhost:3000`
      - Go to "Data Sources" and choose Prometheus as the source.
      - Use `http://prometheus:9090` as the Prometheus server URL.
      - Go to "Dashboards" and create a new dashboard.
      - Create graphs for CSRF failures, total add requests, and the latency of add requests in this dashboard:

        <img width="1621" height="799" alt="image" src="https://github.com/user-attachments/assets/89fc5562-65fb-4deb-ab22-b9a8988feb5b" />
    - To end Prometheus and Grafana services, press `Ctrl+C`.
    - To stop and remove containers, networks, images, and volumes, run the following command:
      ```
      docker compose down
      ```

    - To view logs in Cloud Logging, go to "Monitoring" and then to "Logs Explorer" in the GCP portal:
      - Run the queries for the following:
        - Successful application start:
          ```
          severity="INFO"
          textPayload: "App started successfully"
          ```

          <img width="1861" height="557" alt="image" src="https://github.com/user-attachments/assets/3b1abf98-1861-42fd-b403-afda7564583b" />

        - CSRF failures:
          ```
          severity: "WARNING"
          textPayload: "CSRF failure: "
          ```

          <img width="1825" height="769" alt="image" src="https://github.com/user-attachments/assets/5bafef3e-207f-4a91-bc72-18b4bf2de3a4" />

        - Added requests:
          ```
          severity: "INFO"
          textPayload: "Task added: "
          ```

          <img width="1834" height="606" alt="image" src="https://github.com/user-attachments/assets/96913d92-6375-4970-a8b7-696de6122ce1" />

        - Completed requests:
          ```
          severity: "INFO"
          textPayload: "Task completed: "
          ```

          <img width="1859" height="741" alt="image" src="https://github.com/user-attachments/assets/d6ddbd66-7014-48f7-8fa4-f21bafe18852" />





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
- https://luis-sena.medium.com/creating-the-perfect-python-dockerfile-51bdec41f1c8
- https://docs.docker.com/build/building/best-practices/#run
- https://www.geeksforgeeks.org/python/csrf-protection-in-flask/
- https://flask-wtf.readthedocs.io/en/0.15.x/csrf/
- https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html
- https://flask.palletsprojects.com/en/stable/config/
- https://www.geeksforgeeks.org/python/flask-security-with-talisman/
- https://cloud.google.com/logging/docs/setup/python
- https://prometheus.github.io/client_python/
- https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/import-dashboards/
- https://www.geeksforgeeks.org/cloud-computing/google-cloud-monitoring-google-cloud-logging/
- https://medium.com/@fenari.kostem/monitoring-your-web-app-with-prometheus-and-grafana-a-step-by-step-guide-8286dae606c7
- https://betterstack.com/community/guides/monitoring/prometheus-python-metrics/
- https://grafana.com/docs/grafana-cloud/monitor-applications/asserts/enable-prom-metrics-collection/application-frameworks/flask/
- https://github.com/SigNoz/opentelemetry-collector-prometheus-receiver-example
- https://www.youtube.com/watch?v=moLWjeXoVso
