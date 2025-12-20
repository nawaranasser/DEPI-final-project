#############################
# Security group for Nexus (allow SSH + Nexus UI + Docker registry)
#############################
resource "aws_security_group" "nexus_sg" {
  name        = "nexus-sg"
  description = "Allow SSH and Nexus ports"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Nexus UI"
    from_port   = 8081
    to_port     = 8081
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Nexus Docker registry"
    from_port   = 8083
    to_port     = 8083
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "nexus-sg"
  }
}
#############################
# Persistent EBS volume for Nexus data
#############################

resource "aws_ebs_volume" "nexus_data" {
  availability_zone = "us-east-1a"
  size              = var.nexus_ebs_size # 50
  type              = "gp3"

  tags = {
    Name = "nexus-data-volume"
  }
}
#############################
# EC2 Instance to run Nexus
#############################
resource "aws_instance" "nexus" {
  # Using the Amazon Linux 2023 AMI ID that we confirmed works
  ami                         = "ami-08d7aabbb50c2c24e"
  instance_type               = var.nexus_instance_type # t3.medium
  subnet_id                   = aws_subnet.public.id 
  vpc_security_group_ids      = [aws_security_group.nexus_sg.id]
  associate_public_ip_address = true
  key_name                    = aws_key_pair.bookstore_key.key_name

  tags = {
    Name = "nexus-instance"
  }
}

#############################
# Attach the EBS volume to the Nexus EC2 instance
#############################
resource "aws_volume_attachment" "nexus_attach" {
  device_name  = "/dev/sdf"
  volume_id    = aws_ebs_volume.nexus_data.id
  instance_id  = aws_instance.nexus.id
  force_detach = true
}

