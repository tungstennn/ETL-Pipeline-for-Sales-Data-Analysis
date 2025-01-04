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
