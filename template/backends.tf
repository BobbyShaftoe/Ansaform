terraform {
  backend "s3" {
    bucket = "development-hn-tfstate"
    key = "${var.project}/terraforrm.tfstate"
    region = var.aws_region
  }
}

