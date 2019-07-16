

module "vpc" {
  source              = "./Networking/vpc"
  vpc_id              = var.vpc_id
  cidr                = var.cidr
  internet_gateway_id = var.internet_gateway_id
  networking_tags     = var.networking_tags
}

module "subnet" {
  source          = "./Networking/subnet"
  testing_vpc_id  = module.vpc.testing_vpc_id
  subnet_cidr     = var.subnet_cidr
  az              = var.az
  networking_tags = var.networking_tags
}

module "route" {
  source = "./Networking/route"

  testing_vpc_id         = module.vpc.testing_vpc_id
  testing_route_table_id = module.vpc.testing_route_table_id
  testing_int_gw_id      = module.vpc.testing_int_gw_id
  testing_ext_subnet_ids = [module.subnet.testing_ext_subnet_id_0, module.subnet.testing_ext_subnet_id_1, module.subnet.testing_ext_subnet_id_2]
  testing_int_subnet_ids = [module.subnet.testing_int_subnet_id_3, module.subnet.testing_int_subnet_id_4, module.subnet.testing_int_subnet_id_5]
  networking_tags        = var.networking_tags
}

module "ec2_instances_security_group" {
  source = "./Networking/security_groups"

  vpc_id = module.vpc.testing_vpc_id

  to_port   = "443"
  from_port = "443"
  protocol  = "tcp"
  type      = "ingress"

  networking_tags = var.networking_tags
}

module "ec2_instances" {
  source = "./Compute/ec2_clients"

  ami_id                         = data.aws_ami.centos.image_id
  domain_name                    = var.domain_name
  key_name                       = var.key_name
  security_group_id              = module.ec2_instances_security_group.main_security_group_id
  subnet_id                      = module.subnet.testing_ext_subnet_id_0
  user_data                      = ""
  ebs_root_delete_on_termination = true
  ebs_root_volume_size           = "20"
  ebs_root_volume_type           = "gp2"
  environment                    = "development"
  name                           = var.instance_name
  server_role                    = "testing registry"
  instance_type                  = "t2.micro"
}

