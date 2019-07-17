
aws_id = "088841113972"
aws_region = "us-east-1"
environment = "development"
project = "ansaform"

az = ["us-east-1a", "us-east-1b", "us-east-1c"]

domain_name = "testing-registry.aws-halcyon-infra.net"
hosted_zone_id = "ZXDO38WX4GN6I"

internet_gateway_id = "igw-37888150"

vpc_id = "vpc-22b2cf44"
subnet_id = "subnet-94d1f3b9"

cidr = "10.10.0.0/16"
subnet_cidr = ["10.10.10.0/28", "10.10.10.16/28", "10.10.10.32/28", "10.10.10.48/28", "10.10.10.64/28", "10.10.10.80/28"]

my_ip = ""

security_group_name = ""
security_group_id = "sg-cf2a2bb3"
protocol = ""
from_port = ""
to_port = ""


ami_id = "ami-f6e27ee0"

key_name = "nb-keypair-02"
testing_key_testing_client = "nb-keypair-02"
testing_key_testing_server = "nb-keypair-02"

instance_name = "testing Registry"
application_server_role = "testing Registry"

tags = {
  Name        = "testing_server"
  Role        = "testing_registry"
  Environment = "development"
}

networking_tags = [
  "testing_client",
  "testing_server",
  "testing_deployment",
]

testing_bucket_prefix = "logs"
testing_buckets = ["testing-client-bucket", "testing-server-bucket", "testing-elb-bucket"]
