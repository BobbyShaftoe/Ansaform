data "aws_vpc" "this_vpc" {
  id = var.vpc_id
}


data "aws_internet_gateway" "ig" {
  internet_gateway_id = var.internet_gateway_id
}


resource "aws_vpc_dhcp_options" "testing_vpc_dhcp_id" {
  domain_name = "us-east-1.compute.internal"
  domain_name_servers = [
    "AmazonProvidedDNS"]
  tags = {
    Name = var.networking_tags[0]
    Stack = var.networking_tags[1]
  }
}

