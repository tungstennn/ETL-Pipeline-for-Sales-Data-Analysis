# **ETL Pipeline with AWS Infrastructure**

## **Project Overview**
This project implements an **ETL (Extract, Transform, Load) pipeline** using **AWS services** and **Terraform** for infrastructure as code (IaC). The pipeline extracts raw data from an **S3 bucket**, transforms it using **Python (with Pandas)**, and loads the cleaned data into an **Amazon RDS MySQL database**.

The infrastructure and ETL process are automated and modular, demonstrating a robust approach to handling data engineering workflows.

---

## **Key Features**
- **Infrastructure as Code**:
  - Provisioned using **Terraform**, including:
    - A VPC with public subnets.
    - An S3 bucket for raw data storage.
    - An RDS MySQL instance for storing transformed data.
    - Security groups to manage access control.
  - All infrastructure is automatically created using Terraform.

- **ETL Pipeline**:
  - **Extract**: A CSV file is uploaded to an S3 bucket and extracted programmatically using Python and Boto3.
  - **Transform**: Data is cleaned, validated, and transformed using Pandas.
  - **Load**: The transformed data is inserted into an RDS MySQL database.

- **Modular Scripts**: The ETL pipeline is divided into three Jupyter notebooks:
  1. `01_extract_data.ipynb`: Extracts data from S3 into a Pandas DataFrame.
  2. `02_transform_data.ipynb`: Cleans and transforms the data.
  3. `03_load_data.ipynb`: Loads the transformed data into the RDS MySQL database.

---

## **Project Workflow**

1. **Infrastructure Creation**:
   - S3 bucket is provisioned for raw data storage.
   - RDS MySQL instance is set up with public access (for development purposes).

2. **ETL Process**:
   - **Extract**: The raw CSV file is fetched from the S3 bucket.
   - **Transform**:
     - Handle null values.
     - Standardize date formats.
     - Remove outliers (e.g., filter out sales above a specific threshold).
   - **Load**: The cleaned data is inserted into the `sales_data` table in RDS.

3. **Automation**:
   - Infrastructure creation is automated using Terraform.
   - ETL scripts run sequentially for end-to-end data processing.

---

## **Setup Instructions**

### **Prerequisites**
1. **AWS Account**: Ensure you have access to an AWS account.
2. **Terraform Installed**: [Download and install Terraform](https://developer.hashicorp.com/terraform/downloads).
3. **Python Installed**: Ensure Python 3.8 or higher is installed.
4. **Required Python Packages**:
   Install the following packages using `pip`:
   ```bash
   pip install boto3 pandas pymysql sqlalchemy
