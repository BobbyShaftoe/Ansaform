terraform {
  backend "s3" {
    bucket = "development-ansaform-tfstate"
    key = "development/ansaform/terraforrm.tfstate"
    region = "us-east-1"
  }
}

