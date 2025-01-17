# **ETL Pipeline for Sales Analysis**

## **Project Overview**
This project implements an **ETL (Extract, Transform, Load) pipeline** using **AWS services** and **Terraform** for infrastructure as code (IaC). The pipeline extracts raw data from an **S3 bucket**, transforms it using **Python (with Pandas)**, and loads the cleaned data into an **Amazon RDS MySQL database**.

---

## **Key Features**
- **Infrastructure as Code**:
  - Provisioned using **Terraform**, including:
    - A VPC with public subnets
    - An S3 bucket for raw data storage
    - An RDS MySQL instance for storing transformed data
    - Security groups to manage access control
  - All infrastructure is automatically created using Terraform

- **ETL Pipeline**:
  - **Extract**: A CSV file is uploaded to an S3 bucket and extracted programmatically using Python and Boto3
  - **Transform**: Data is cleaned, validated, and transformed using Pandas
  - **Load**: The transformed data is inserted into an RDS MySQL database

- **Modular Scripts**: The three explanatory (and functional) Jupyter notebooks:
  1. `01_extract_data.ipynb`: Extracts data from S3 into a Pandas DataFrame
  2. `02_transform_data.ipynb`: Cleans and transforms the data
  3. `03_load_data.ipynb`: Loads the transformed data into the RDS MySQL database
- **Production-ready Script**:
  - Final single `etl_pipeline.py` script that integrates all the the processes from the notebooks
  - Cohesive file that represents production-ready code for seamless execution
---

## **Simplified Project Workflow**

```mermaid
flowchart TD
    A((Start: Terraform Infrastructure Setup)) --> B[Provision S3 Bucket & RDS with Terraform]
    B --> C[Upload Raw CSV to S3 Bucket]
    C --> D[Extract Data from S3]
    D --> E[Transform Data with Pandas]
    E --> F[Load Data into RDS MySQL]
    F --> G([Deploy & Automate Pipeline])
```
---

## **Areas to Improve**

1. **Testing**:
   - Implement unit and integration tests for the ETL pipeline to ensure data quality and handle edge cases (e.g., corrupted files, invalid data formats, or missing values)
   - Create a test environment to simulate the infrastructure, ensuring that the pipeline runs correctly before deploying to production

2. **CI/CD Implementation**:
   - Set up a CI/CD pipeline (e.g., using GitHub Actions) to fully automate the deployment of Terraform infrastructure and the ETL pipeline. This would allow for smoother updates, quicker deployments, and enhanced collaboration

3. **Security Group Improvements**:
   - Restrict the security group to allow access only from specific IP addresses (e.g., your local IP) instead of opening it to the entire internet (`0.0.0.0/0`). This change will greatly enhance security and prevent unauthorized access
   - Automate the security group configuration to dynamically update the allowed IP based on the developer’s current public IP

4. **Improved ETL Triggers**:
   - Instead of manually triggering the ETL pipeline, implement an **AWS Lambda function** or a scheduled job to automatically start the ETL process when a new file is uploaded to the S3 bucket

5. **Data Visualization**:
    - Enhance the project by integrating a visualization tool (**Tableau**) to create dashboards and meaningful insights from the transformed data in the RDS database

