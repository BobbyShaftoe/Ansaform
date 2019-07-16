# Create security groups and open port
resource "aws_security_group" "testing_security_group_elb" {
  name = "_elb"
  description = "front server security group"
  vpc_id = var.testing_vpc_id
  ingress {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    security_groups = [
      var.testing_security_group_web]
  }
  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = [
      var.cidr]
  }
  tags {
    Name = var.networking_tags[0]
  }
}
