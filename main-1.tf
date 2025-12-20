# Specify the AWS Provider and its version
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }

    nexus = {
      source  = "datadrivers/nexus"
      version = "~> 1.21"
    }
  }
}
# Configure the AWS Provider
provider "aws" {
  region = var.aws_region
}

# Nexus provider — uses variables for URL and credentials
provider "nexus" {
  url = var.nexus_url
}






