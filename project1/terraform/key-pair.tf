# resource "aws_key_pair" "nora_key" {
#   key_name   = "nora-bookstore"
#   public_key = file("~/.ssh/nora-bookstore.pub")
# }
resource "aws_key_pair" "bookstore_key" {
  key_name   = "bookstore-terraform-key"
  public_key = file("~/.ssh/bookstore-terraform.pub")

  tags = {
    Name = "bookstore-terraform-key"
  }
}
