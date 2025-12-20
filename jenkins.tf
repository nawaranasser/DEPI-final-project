# Security Group for Jenkins Server
resource "aws_security_group" "jenkins_sg" {
  name        = "jenkins-sg"
  description = "Security group for Jenkins server"
  vpc_id      = aws_vpc.main.id   # use your existing VPC

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Jenkins UI"
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 50000
    to_port     = 50000
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
    Name = "jenkins-sg"
  }
}
#############################################
# IAM Policy for EKS access
resource "aws_iam_policy" "jenkins_eks_policy" {
  name        = "JenkinsEKS-Policy"
  description = "Full EKS access for Jenkins CI/CD"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow",
        Action = [
            "eks:*"    
        ],
        Resource = "*"
      },
      {
        Effect = "Allow",
        Action = [
          "sts:GetCallerIdentity",
          "iam:PassRole"
        ],
        Resource = "*"
      }
    ]
  })
}

###########################################################

# IAM Role for Jenkins Server
resource "aws_iam_role" "jenkins_role" {
  name = "jenkins-role2"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}


##################################################
# Attach the new EKS policy to the Jenkins Role
resource "aws_iam_role_policy_attachment" "jenkins_eks_policy_attachment" {
  role       = aws_iam_role.jenkins_role.name
  policy_arn = aws_iam_policy.jenkins_eks_policy.arn
}
################################################

# Attach SSM Managed Instance Core Policy to Jenkins Role
resource "aws_iam_role_policy_attachment" "jenkins_ssm" {
  role      = aws_iam_role.jenkins_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}
resource "aws_iam_role_policy_attachment" "jenkins_eks_access" {
  role       = aws_iam_role.jenkins_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
}
# IAM Instance Profile for Jenkins Server
resource "aws_iam_instance_profile" "jenkins_profile" {
  name = "jenkins-instance-profile"
  role = aws_iam_role.jenkins_role.name
}

# Jenkins EC2 Instance
resource "aws_instance" "jenkins" {
  ami                    = "ami-08d7aabbb50c2c24e"
  instance_type          = var.nexus_instance_type # t3.medium
  subnet_id              = aws_subnet.public.id   # public subnet
  vpc_security_group_ids = [aws_security_group.jenkins_sg.id]
  key_name               = aws_key_pair.bookstore_key.key_name


  iam_instance_profile = aws_iam_instance_profile.jenkins_profile.name

  tags = {
    Name = "jenkins-server"
  }
}

