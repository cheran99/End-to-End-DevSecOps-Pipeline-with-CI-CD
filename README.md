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

Ensure that you are in the directory for this GitHub repo in the WSL terminal. Once you are in this directory, change the directory to the `terraform` directory using the following command:
```
cd terraform
```

Once you are in this directory, initialise Terraform using the following command:
```
terraform init
```

Once Terraform is initialised, open the `main.tf` file in the GitHub repo. 








## References
- https://squareops.com/ci-cd-security-devsecops/#:~:text=Why%20SquareOps%20is%20the%20Right,security%20for%20your%20software%20delivery.
- https://www.microsoft.com/en-gb/security/business/security-101/what-is-devsecops#:~:text=DevSecOps%2C%20which%20stands%20for%20development,releasing%20code%20with%20security%20vulnerabilities.
