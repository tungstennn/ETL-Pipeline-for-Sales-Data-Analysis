# Global variables_______________________

variable "region" {
  description = "AWS region"
  type        = string
  default     = "eu-west-2"
}

# S3 variables__________________________

variable "bucket_name" {
  description = "S3 bucket name"
  type        = string
  default     = "tungstennn-bucket"
}

# RDS variables_________________________

variable "db_username" {
  description = "Username for the database"
  type        = string
}

variable "db_password" {
  description = "Password for the database"
  type        = string
}

variable "cidr_block" {
  description = "List of CIDR blocks for database access"
  type        = string
  default     = "10.1.0.0/16"
}

variable "subnet_cidr_blocks" {
  description = "List of subnet CIDR blocks"
  type        = list(string)
  default     = ["10.1.3.0/24","10.1.2.0/24"]
}

variable "vpc_name" {
  description = "Name for the VPC"
  type        = string
  default     = "tungstennn-vpc"
}