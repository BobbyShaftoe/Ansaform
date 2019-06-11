# ---------------------------------------------------------------------------------------------------------------------
# terraform -var-file plan

variable "environment" {}


variable "instance_name" {
  description = "The Name tag to set for the EC2 Instance."
  default     = "terratest-example"
}

variable "aws_region" {}
variable "account_id" {}

variable "service_types" {
  type = "map"
  default = {
    terratest-example = "example service"
    terratest-monitor = "monitoring service"
  }
}




