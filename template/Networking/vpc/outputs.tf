output "testing_vpc_id" {
//  value = "${aws_vpc.testing_vpc_id.id}"
  value = data.aws_vpc.this_vpc.id
}

output "testing_int_gw_id" {
//  value = "${aws_internet_gateway.testing_int_gw_id.id}"
  value = data.aws_internet_gateway.ig.internet_gateway_id
//  value = "${aws_internet_gateway.testing_int_gw_id.id}"
}

output "testing_route_table_id" {
  value = data.aws_vpc.this_vpc.main_route_table_id
}

output "testing_vpc_dhcp_id" {
  value = data.aws_vpc.this_vpc.dhcp_options_id
}

