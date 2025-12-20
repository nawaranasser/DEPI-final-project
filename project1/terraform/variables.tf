variable "aws_region" {
  description = "The AWS region where resources will be created"
  type        = string
  default     = "us-east-1"
}


variable "nexus_url" {
  description = "Base URL of the Nexus repository manager (e.g. https://nexus.example.com)"
  type        = string
  default     = null
}

variable "nexus_instance_type" {
  description = "EC2 instance type for Nexus"
  type        = string
  default     = "t3.medium"
}

variable "nexus_ebs_size" {
  description = "Size (GB) of the EBS volume for Nexus data"
  type        = number
  default     = 50
}

variable "nexus_admin_password" {
  type    = string
  default = "Admin123"
}


variable "eks_cluster_name" {
  description = "Name of the EKS cluster Jenkins will interact with"
  type        = string
  default     = "bookstore-eks"
}
