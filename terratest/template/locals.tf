

locals {
  tag_map = {
    environment = "${var.environment}"
    service_type = "default"
  }
}

