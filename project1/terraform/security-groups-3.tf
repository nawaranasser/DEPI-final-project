#####################################
# Frontend Security Group (Tier 1)
#####################################
resource "aws_security_group" "frontend_sg" {
  name        = "frontend-sg"
  description = "Allow HTTP for Frontend"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "HTTP from Internet"
    from_port   = 80
    to_port     = 80
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
    Name = "frontend-sg"
  }
}

#####################################
# Backend Security Group (Tier 2)
#####################################
resource "aws_security_group" "backend_sg" {
  name        = "backend-sg"
  description = "Allow traffic from Frontend SG"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "Allow API access from Frontend"
    from_port       = 5000
    to_port         = 5000
    protocol        = "tcp"
    security_groups = [aws_security_group.frontend_sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "backend-sg"
  }
}

#####################################
# Database Security Group (Tier 3)
#####################################
resource "aws_security_group" "database_sg" {
  name        = "database-sg"
  description = "Allow MySQL access from Backend SG"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "MySQL from Backend"
    from_port       = 3306
    to_port         = 3306
    protocol        = "tcp"
    security_groups = [aws_security_group.backend_sg.id]
  }

  tags = {
    Name = "database-sg"
  }
}
