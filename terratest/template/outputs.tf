
output "ec2_instance_id" {
  value = "${aws_instance.example.id}"
}

output "ec2_ami_image" {
  value = "${aws_instance.example.ami}"
}

output "ec2_az" {
  value = "${aws_instance.example.availability_zone}"
}


