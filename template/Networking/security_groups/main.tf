
# Create security groups and open port

resource "aws_security_group" "main_security_group" {
  name = var.security_group_name
  description = "front server security group"
  vpc_id = var.vpc_id

  tags = {
    Name = var.networking_tags[0]
    Stack = var.networking_tags[1]
  }
}



resource "aws_security_group_rule" "main_security_group_rule" {

  description = "Security group rule for main security group"
  from_port = var.from_port
  protocol = var.protocol
  to_port = var.to_port
  type = "ingress"

  cidr_blocks = ["10.0.0.0/8"]

  security_group_id = aws_security_group.main_security_group.id
}


