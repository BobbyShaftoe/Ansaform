
data "aws_ami" "centos" {
  most_recent = true
  owners = ["aws-marketplace"]

  filter {
    name = "product-code"
    values = [
      "aw0evgkw8e5c1q413zgy5pjce"]
  }
}

