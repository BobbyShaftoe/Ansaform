


variable "vpc_id" {
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

variable "type" {
  default = ""
}



variable "networking_tags" {
  type = "list"
}

