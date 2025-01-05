# Output the RDS instance endpoint
output "rds_endpoint" {
  value       = aws_db_instance.rds_instance.endpoint
  description = "The endpoint of the RDS instance"
}

output "vpc_id" {
    value       = aws_vpc.main.id
    description = "The ID of the VPC"
}

# output "subnet_id" {
#     value       = aws_subnet.public_subnet.id
#     description = "The ID of the subnet"
# }