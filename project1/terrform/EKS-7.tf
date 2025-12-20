# EKS IAM Roles
#####################################################
# This role allows EKS service to create/manage AWS resources on your behalf
resource "aws_iam_role" "eks_cluster_role" {
  name = "eks-cluster-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "eks.amazonaws.com"
        }
      }
    ]
  })
}

# attach role to cluseter
# Attach the standard EKS cluster policy to the cluster role
# This gives EKS permissions to manage cluster resources
resource "aws_iam_role_policy_attachment" "eks_cluster_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.eks_cluster_role.name
}

#node role
# EKS Node Group IAM Role
# This role will be used by EC2 instances (worker nodes) in the node group
resource "aws_iam_role" "eks_node_role" {
  name = "eks-node-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

#attach worker node role to node
# Policy 1: Allows worker nodes to connect to EKS cluster

resource "aws_iam_role_policy_attachment" "eks_worker_node_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.eks_node_role.name
}

# attach cni role to node
# Policy 2: Allows networking for pods (assign IPs, manage ENIs)

resource "aws_iam_role_policy_attachment" "eks_cni_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
  role       = aws_iam_role.eks_node_role.name
}

# Policy 3: Allows nodes to pull Docker images from ECR

resource "aws_iam_role_policy_attachment" "ec2_container_registry_readonly" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.eks_node_role.name
}

# resource "aws_iam_policy" "jenkins_eks_policy" {
#   name = "JenkinsEKS-Policy-${terraform.workspace}"
# }

##################################################

# EKS Cluster
# This is the Kubernetes control plane (API server, etcd, controllers)
resource "aws_eks_cluster" "bookstore" {
  name     = "bookstore-eks"
  role_arn = aws_iam_role.eks_cluster_role.arn

  vpc_config {
    subnet_ids = [
      aws_subnet.private.id,
      aws_subnet.private_2.id
    ]
    endpoint_private_access = true
    endpoint_public_access  = true
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks_cluster_policy
  ]
}

# Launch Template for EKS Nodes allow http access to nexus
resource "aws_launch_template" "eks_nodes" {
  name_prefix = "eks-http-nexus-"

  user_data = base64encode(<<-EOF
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="==MYBOUNDARY=="

--==MYBOUNDARY==
Content-Type: text/x-shellscript; charset="us-ascii"

#!/bin/bash
set -o xtrace

cat <<EOT > /etc/containerd/config.toml
version = 2

[plugins."io.containerd.grpc.v1.cri".registry]
  [plugins."io.containerd.grpc.v1.cri".registry.mirrors]
    [plugins."io.containerd.grpc.v1.cri".registry.mirrors."44.202.103.178:8083"]
      endpoint = ["http://44.202.103.178:8083"]
EOT

systemctl restart containerd

--==MYBOUNDARY==--
EOF
  )

  lifecycle {
    create_before_destroy = true
  }
}


# EKS Node Group
# These are the worker nodes that run your pods/containers

resource "aws_eks_node_group" "nodes" {
  cluster_name    = aws_eks_cluster.bookstore.name
  node_group_name = "bookstore-nodes"
  node_role_arn   = aws_iam_role.eks_node_role.arn
  subnet_ids      = [aws_subnet.private.id, aws_subnet.private_2.id]

  scaling_config {
    desired_size = 2
    max_size     = 3
    min_size     = 1
  }

  instance_types = ["t3.medium"]
  launch_template {
    id      = aws_launch_template.eks_nodes.id
    version = "$Latest"
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks_worker_node_policy,
    aws_iam_role_policy_attachment.eks_cni_policy,
    aws_iam_role_policy_attachment.ec2_container_registry_readonly
  ]
}






