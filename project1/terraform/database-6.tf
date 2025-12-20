############################################
# DB Subnet Group (uses private subnets)
############################################
resource "aws_db_subnet_group" "database" {
  name = "bookstore-db-subnet-group"
  subnet_ids = [
    aws_subnet.private.id,
    aws_subnet.private_2.id
  ]

  tags = {
    Name = "Bookstore DB Subnet Group"
  }
}

############################################
# Database Security Group (already in security-groups.tf)
# aws_security_group.database_sg
############################################


############################################
# RDS MySQL Instance
############################################
resource "aws_db_instance" "mysql" {
  allocated_storage = 20
  storage_type      = "gp2"
  engine            = "mysql"
  engine_version    = "8.0"
  instance_class    = "db.t3.micro"
  db_name           = "bookstore"

  username = "admin"
  password = "MyBookstoreDB123"

  parameter_group_name = "default.mysql8.0"
  skip_final_snapshot  = true

  db_subnet_group_name   = aws_db_subnet_group.database.name
  vpc_security_group_ids = [aws_security_group.database_sg.id]

  tags = {
    Name = "bookstore-mysql-db"
  }
}
