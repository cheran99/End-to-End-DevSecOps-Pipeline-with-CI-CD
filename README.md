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









## References
- https://squareops.com/ci-cd-security-devsecops/#:~:text=Why%20SquareOps%20is%20the%20Right,security%20for%20your%20software%20delivery.
- https://www.microsoft.com/en-gb/security/business/security-101/what-is-devsecops#:~:text=DevSecOps%2C%20which%20stands%20for%20development,releasing%20code%20with%20security%20vulnerabilities.
