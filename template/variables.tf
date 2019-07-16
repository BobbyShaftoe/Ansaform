
variable environment {
  default = ""
}

variable "aws_id" {
  description = "AWS ROOT ID"
  default = ""
}

variable "aws_region" {
  description = "AWS region to operate"
  default = ""
}

variable "az" {
  description = "Avalability Zones"
  type = "list"
  default = []
}

variable "vpc_id" {
  default = ""
}

variable "internet_gateway_id" {}

variable "cidr" {
  description = "CIDR for the whole VPC"
  default = ""
}

variable subnet_id {
  default = ""
}

variable "subnet_cidr" {
  description = "CIDR_AZ"
  type = "list"
  default = []
}

variable domain_name {
  default = ""
}

variable hosted_zone_id {
  default = ""
}


variable security_group_id {
  default = ""
}

variable "security_group_name" {
  default = ""
}
variable "from_port" {
  default = ""
}
variable "protocol" {
  default = ""
}
variable "to_port" {
  default = ""
}

variable "my_ip" {
  description = "My app to allow to connect to security group"
  default = ""
}




variable ami_id {
  default = ""
}

variable key_name {
  default = "nb-keypair-02"
}

variable instance_name {
  default = "testing Registry"
}


variable "tags" {
  type = "map"
}

variable "networking_tags" {
  type = "list"
  default = []
}



variable "testing_buckets" {
  description = "bucket for access logs"
  type = "list"
  default = []
}

variable "testing_bucket_prefix" {
  description = "bucket prefix for access logs"
  default = "logs"
}



variable "testing_key_testing_client" {
  description = "key to use for testing clients"
  default = "nb-keypair-02"
}

variable "testing_key_testing_server" {
  description = "key to use for testing servers"
  default = "nb-keypair-02"
}

variable application_server_role {
  default = "testing Registry"
}


