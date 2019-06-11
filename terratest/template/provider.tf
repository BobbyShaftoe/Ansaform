provider "aws" {
  region = "${var.aws_region}"
  shared_credentials_file = "/Users/nicksinclair/.aws/credentials"
  profile = "default"
}

