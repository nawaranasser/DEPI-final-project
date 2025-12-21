# 📚 Full-Cycle Bookstore Automation

A complete end-to-end DevOps project that demonstrates the full software delivery lifecycle — from building a simple bookstore application to automating infrastructure provisioning, CI/CD pipelines, containerization, and Kubernetes deployment on AWS.

This repository showcases **two different DevOps implementations** using modern tools and best practices.

---

# 📌 Project Overview

This initiative establishes a robust DevOps pipeline for a modern bookstore application on AWS, employing Infrastructure as Code (IaC) principles. We utilise Terraform to provision a production-grade Amazon EKS cluster, complete with essential networking, security, and load-balancing configurations.

GitHub Actions orchestrates the entire Software Delivery Life Cycle (SDLC), from code commits to container image builds, infrastructure deployments, and application rollouts. The bookstore application, composed of frontend and backend microservices, is managed within Kubernetes, with automated deployments driven by Ansible playbooks.

This comprehensive DevOps approach demonstrates how to achieve rapid, reliable, and scalable application delivery while maintaining IaC and robust CI/CD practices.

---

# 📌 Architecture diagrams:
### Diagram of Project 1:

![Project Diagram](Diagram1.png)

### Diagram of Project 2:

![Project Diagram](Diagram2.png)


# 🏗️ High-Level Architecture

**Cloud Provider:** AWS  
**Orchestration:** Kubernetes (EKS)

Main components:
- AWS VPC with public & private subnets
- NAT Gateway, Route Tables, Internet Gateway
- EC2 instances
- Amazon EKS cluster with managed node groups
- Application Load Balancer or Cluster Load Balancer
- CI/CD pipelines
- Artifact & container registries

  ---

# 📂 Repository Structure

```bash
.
DEPI-final-project/
├── Project1/
│   ├── terraform/             # Terraform scripts for AWS infrastructure
│   ├── ansible/               # Ansible playbooks for configuration
│   ├── Jenkimsfile            # Jenkins pipeline definition
│   └── k8s/                   # Kubernetes manifests for deployment
│
│
├── Project-2/
│   ├── bookstore-devops/
│   │   ├── terraform/             # Terraform scripts for AWS infrastructure
│   │   ├── ansible/               # Ansible playbooks
│   │   ├── github-actions/        # GitHub Actions workflows for CI/CD
│   │   └── kubernetes/            # Kubernetes manifests for deployment
│   │
│   └── bookstore-app-v2/
│       ├── backend/               # Backend code for bookstore application
│       ├── frontend/              # Frontend code for bookstore application
│       ├── Dockerfile             # Dockerfile for containerizing the app
│       └── README.md              # Optional README for the app itself
│
├── Diagram1.png                   # Architecture diagram for Project 1
├── Diagram2.png                   # Architecture diagram for Project 2
│
└── README.md                  # Root README.md covering full project

```

---

# 🧭 Project Phases Overview

## Prject 1 Phases:

| Phase | Stage | Tool | Purpose |
|------|-------|------|---------|
| Phase 1 | Development | Local Repository | Application code development |
| Phase 2 | Infrastructure | Terraform | Provision AWS resources |
| Phase 3 | Configration | Ansible | configure jenkins and nexus servers |
| Phase 4 | Pipeline | Jenkins | Build and Push docker images to nexus repo then connect to EKS deployment |
| Phase 5 | Deployment | Amazon EKS | manage application containers then deply using loud balancer k8s service|

## Prject 2 Phases:

| Phase | Stage | Tool | Purpose |
|------|-------|------|---------|
| Phase 1 | Development | Local Repository | Application code development |
| Phase 2 | Infrastructure | Terraform | Provision AWS resources |
| Phase 3 | CI/CD Pipeline | GitHub Actions | Build and push Docker images |
| Phase 4 | Registry | Amazon ECR | Store and manage Docker images |
| Phase 5 | Configuration | Ansible | Configure systems and apply Kubernetes manifests |
| Phase 6 | Deployment | Amazon EKS | Run and manage application containers |

---
# ▶️ How to run the projects 

## Project 1 

1️⃣ Prepare Environment

Install Terraform and AWS CLI

Configure AWS credentials: aws configure

2️⃣ Initialize Terraform : terraform init

3️⃣ Review Execution Plan : terraform plan

4️⃣ Apply Configuration : terraform apply

5️⃣ Verify Resources

EKS Cluster

aws eks update-kubeconfig --region <region> --name bookstore-eks
kubectl get nodes

Jenkins URL: http://<jenkins_public_ip>:8080

Nexus URL: http://<nexus_public_ip>:8081

6️⃣ Run the Ansibe playbok to configure Nexus : ansibel-playbook -i invintory.ini nexus-playbook.yml

7️⃣ Run the Ansibe playbok to configure Nexus : ansibel-playbook -i invintory.ini nexus-playbook.yml

8️⃣ Follow URL in the terraform output to open jenkins & nexus servers :  Nexus URL: http://<nexus_public_ip>:8081 , Jenkins URL: http://<jenkins_public_ip>:8080

9️⃣ SSH into Jenkins EC2 : ssh -i your-key.pem ec2-user@ip-Jenkins

Run these commands inside the jenkins container :

1- sudo vi /etc/docker/daemon.json
{
  "insecure-registries": ["ip-nexus:8083"]
}

2- sudo systemctl restart docker

3- docker login ip-nexus:8083

    username: admin
    password: Admin123
    -->>Login Succeeded

4- in your local machine Run :
 
 - kubectl edit configmap aws-auth -n kube-system
       
        apiVersion: v1
        data:
        mapRoles: |
          - rolearn: arn:aws:iam::992487937555:role/eks-node-role
            username: system:node:{{EC2PrivateDNSName}}
            groups:
              - system:bootstrappers
              - system:nodes
      
          - rolearn: arn:aws:iam::992487937555:role/jenkins-role      #add this
            username: jenkins
            groups:
              - system:masters

5 -  SSH into Jenkins EC2 again
  -  kubectl get nodes
  - aws sts get-caller-identity
    
  -->> if work 

  - kubectl create secret docker-registry nexus-secret \
     --docker-server=nexus-ip:8083 \
     --docker-username=admin \
     --docker-password='Admin123' \
     --namespace=bookstore

  - kubectl get svc bookstore-frontend
6 - COPY the Extrnal IP and open it in any browser -> NOW your app is LIVE






# 📦 Bookstore Infrastructure Provisioning with Terraform, EKS, Jenkins, and Nexus

This repository contains Terraform scripts to provision a **secure multi-tier AWS infrastructure** for a bookstore application, including networking, EKS cluster, Jenkins, Nexus, and RDS.

---

## 🎯 Outcomes

### Networking
- **Public subnets:** Direct internet access.
- **Private subnets:** Route traffic through NAT.
- **Architecture:** Secure multi-tier design established.

### Security Groups
- **Frontend:** Accessible on HTTP (port 80).
- **Backend:** Communicates only with Frontend (port 5000).
- **Jenkins & Nexus:** Secured with SSH and application ports.

### EKS
- Fully provisioned **Kubernetes cluster**.
- Worker nodes with proper **IAM roles** and networking.
- Cluster ready for **container deployment**.

### Jenkins
- EC2 instance up and running.
- Full access to EKS for **CI/CD pipelines**.
- Secure **SSM access** enabled.

### Nexus
- EC2 instance hosting **Docker registry**.
- Persistent **EBS volume** attached for data durability.
- Accessible for **pushing/pulling images**.

### Outputs
- **RDS endpoint:** `rds_endpoint`
- **Nexus public IP & URL:** `nexus_public_ip`, `nexus_url`
- **Jenkins public IP & URL:** `jenkins_public_ip`, `jenkins_url`
- **EKS cluster endpoint & name:** `eks_cluster_endpoint`, `eks_cluster_name`

---

## ▶️ How to Run

### 1️⃣ Prepare Environment
- Install [Terraform](https://www.terraform.io/) and [AWS CLI](https://aws.amazon.com/cli/).
- Configure AWS credentials:

```bash
aws configure

---
# 🔮 Future Improvements

• Improvement in Application

• Add monitoring with Prometheus & Grafana

• Add more features

---

# ▶️ Project 1 Resources:

[!🎬[Demo Video](https://drive.google.com/file/d/18imYXqB4_ruSp2dD68rEinkiTgiUTp2l/view?usp=sharing)]

---

# 👨‍💻 Contributors

• **Nora Nasser** - DevOps Engineer

• **Nada Hussien** - DevOps Engineer

• **Hagar Mohamed** - DevOps Engineer
