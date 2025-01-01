# Create an S3 bucket___________________________________________________________________

resource "aws_s3_bucket" "tf-bucket-tungstennn" {
  bucket = var.bucket_name
  tags = {
    Name = var.bucket_name
  }
}

# Enable versioning

resource "aws_s3_bucket_versioning" "versioning" {
  bucket = var.bucket_name
  versioning_configuration {
    status = "Enabled"
  }
}

# Add the raw data file in data folder to the bucket

resource "aws_s3_object" "provision_source_files" {
  bucket = aws_s3_bucket.tf-bucket-tungstennn.bucket
  key    = "messy_raw_data.csv"         # The S3 object key (this is the file name in the bucket)
  source = "../data/messy_raw_data.csv" # Local path to the CSV file in your project folder
}

# Create a Security Group for the RDS instance___________________________________________
resource "aws_security_group" "rds_sg" {
  name        = "rds-sg"
  description = "Security group for RDS instance"

  # Allow inbound MySQL traffic
  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Allow connections from any IP (Not best practice)
  }

  # Allow all outbound traffic (optional, but typically required)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


# Create an RDS instance________________________________________________________________

# resource "aws_db_instance" "rds_instance" {
#   allocated_storage      = 10
#   db_name                = "mydb"
#   engine                 = "mysql"
#   engine_version         = "8.0"
#   instance_class         = "db.t3.micro"
#   username               = "tungstennnuser1"
#   password               = var.db_password
#   publicly_accessible    = false
#   parameter_group_name   = "default.mysql8.0"
#   skip_final_snapshot    = true
#   vpc_security_group_ids = [aws_security_group.rds_sg.id]
#   storage_encrypted      = true

#   tags = {
#     Name = "${var.db_username}-instance"
#   }
# }
