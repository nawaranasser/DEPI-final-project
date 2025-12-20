output "rds_endpoint" {
  description = "The connection endpoint for the RDS database"
  value       = aws_db_instance.mysql.endpoint
  sensitive   = true
}


output "nexus_public_ip" {
  description = "Public IP of the Nexus EC2 instance"
  value       = aws_instance.nexus.public_ip
}

output "nexus_url" {
  description = "Nexus Docker registry URL (use this for image pushes/pulls)"
  value       = "http://${aws_instance.nexus.public_ip}:8081"
}

output "eks_cluster_endpoint" {
  description = "Endpoint for EKS cluster"
  value       = aws_eks_cluster.bookstore.endpoint
}

output "eks_cluster_name" {
  description = "Kubernetes Cluster Name"
  value       = aws_eks_cluster.bookstore.name
}

output "jenkins_public_ip" {
  description = "Public IP of the Jenkins EC2 instance"
  value       = aws_instance.jenkins.public_ip
}

output "jenkins_url" {
  description = "Jenkins URL"
  value       = "http://${aws_instance.jenkins.public_ip}:8080"
}
