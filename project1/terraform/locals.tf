locals {
  nexus_url = "http://${aws_instance.nexus.public_ip}:8081"
}
