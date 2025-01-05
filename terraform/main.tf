# Creating a VPC____________________

resource "aws_vpc" "main" {
  cidr_block           = var.cidr_block #"10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = var.vpc_name
  }
}

# Create public subnet 1

resource "aws_subnet" "public_subnet_1" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.subnet_cidr_blocks[0]
  availability_zone       = "eu-west-2a"
  map_public_ip_on_launch = true

  tags = {
    Name = "public-subnet-2a"
  }
}

# Create public subnet 2

resource "aws_subnet" "public_subnet_2" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.subnet_cidr_blocks[1]
  availability_zone       = "eu-west-2b"
  map_public_ip_on_launch = true

  tags = {
    Name = "public-subnet-2b"
  }
}

# Creating an IGW and attach to VPC

resource "aws_internet_gateway" "my_igw" {
  vpc_id = aws_vpc.main.id
  count  = 1

  tags = {
    Name = "my-igw"
  }
}

# creating route table

resource "aws_route_table" "my_route_table" {
  count  = 1
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0" # Represents all traffic destined for outside the VPC
    gateway_id = aws_internet_gateway.my_igw[0].id
  }
  tags = {
    Name = "my-rt"
  }
}

# Associate route table with subnet

resource "aws_route_table_association" "public_association_1" {
  subnet_id      = aws_subnet.public_subnet_1.id
  route_table_id = aws_route_table.my_route_table[0].id
}

resource "aws_route_table_association" "public_association_2" {
  subnet_id      = aws_subnet.public_subnet_2.id
  route_table_id = aws_route_table.my_route_table[0].id
}


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
  vpc_id      = aws_vpc.main.id


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




# Create an RDS instance and subnet group______________________________________________

# Create a DB Subnet Group
resource "aws_db_subnet_group" "rds_subnet_group" {
  name       = "rds-subnet-group"
  subnet_ids = [aws_subnet.public_subnet_1.id, aws_subnet.public_subnet_2.id]
  tags = {
    Name = "RDS Subnet Group"
  }
}

resource "aws_db_instance" "rds_instance" {
  allocated_storage      = 10
  db_name                = "mydb"
  engine                 = "mysql"
  engine_version         = "8.0"
  instance_class         = "db.t3.micro"
  username               = "tungstennnuser1"
  password               = var.db_password
  publicly_accessible    = true
  parameter_group_name   = "default.mysql8.0"
  skip_final_snapshot    = true
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  storage_encrypted      = true
  db_subnet_group_name   = aws_db_subnet_group.rds_subnet_group.name

  tags = {
    Name = "${var.db_username}-instance"
  }
}
