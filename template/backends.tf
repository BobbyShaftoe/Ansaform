terraform {
  backend "s3" {
    bucket = "development-hn-tfstate"
    key = "development/ansaform/terraforrm.tfstate"
    region = "us-east-1"
  }
}

