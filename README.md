# 📚 Full-Cycle Bookstore Automation

A complete end-to-end DevOps project that demonstrates the full software delivery lifecycle — from building a simple bookstore application to automating infrastructure provisioning, CI/CD pipelines, containerization, and Kubernetes deployment on AWS.

This repository showcases **two different DevOps implementations** using modern tools and best practices.

---

## 📌 Project Overview

This initiative establishes a robust DevOps pipeline for a modern bookstore application on AWS, employing Infrastructure as Code (IaC) principles. We utilise Terraform to provision a production-grade Amazon EKS cluster, complete with essential networking, security, and load-balancing configurations.

GitHub Actions orchestrates the entire Software Delivery Life Cycle (SDLC), from code commits to container image builds, infrastructure deployments, and application rollouts. The bookstore application, composed of frontend and backend microservices, is managed within Kubernetes, with automated deployments driven by Ansible playbooks.

This comprehensive DevOps approach demonstrates how to achieve rapid, reliable, and scalable application delivery while maintaining IaC and robust CI/CD practices.

---

## 🏗️ High-Level Architecture

**Cloud Provider:** AWS  
**Orchestration:** Kubernetes (EKS)

Main components:
- AWS VPC with public & private subnets
- NAT Gateway, Route Tables, Internet Gateway
- EC2 instances
- Amazon EKS cluster with managed node groups
- Application Load Balancer
- CI/CD pipelines
- Artifact & container registries

## 📌 Architecture diagrams:
### Diagram of Project 1:
![Project Diagram](Project_Diagram.png)

### Diagram of Project 2:
![Project Diagram](Project_Diagram.png)

---

## 📂 Repository Structure

```bash
.
├── bookstore-app/
│   ├── backend/
│   ├── frontend/
│   ├── Dockerfile
│   └── README.md
│
├── devops-project-1-jenkins-nexus/
│   ├── terraform/
│   ├── ansible/
│   ├── Jenkimsfile
│   └── k8s/   
│
├── devops-project-2-github-actions-ecr/
│   ├── terraform/
│   ├── ansible/
│   ├── github-actions/
│   └── kubernetes/    
│
├── diagrams/
│   └── architecture.png
│
└── README.md
```

---

## 🔮 Future Improvements

• Improvement in Application

• Add monitoring with Prometheus & Grafana

• Add more features

---

## 👨‍💻 Contributors

• **Nora Nasser** - DevOps Engineer

• **Nada Hussien** - DevOps Engineer

• **Hagar Mohamed** - DevOps Engineer
