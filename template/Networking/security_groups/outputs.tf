output "main_security_group_id" {
  value = aws_security_group.main_security_group.id
}

output "main_security_group_rule_id" {
  value = aws_security_group_rule.main_security_group_rule.id
}


output "main_security_group_rule_from_port" {
  value = aws_security_group_rule.main_security_group_rule.from_port
}

output "main_security_group_rule_to_port" {
  value = aws_security_group_rule.main_security_group_rule.to_port
}


output "main_security_group_rule_description" {
  value = aws_security_group_rule.main_security_group_rule.description
}



