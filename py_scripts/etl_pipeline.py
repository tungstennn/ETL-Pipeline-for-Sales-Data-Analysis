import pandas as pd
import boto3
from sqlalchemy import create_engine
import logging
import os
import pymysql
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ------------------- Extraction Functions -------------------
def extract_csv_from_s3(bucket_name, file_key):
    # Extract CSV file from S3 bucket
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket_name, Key=file_key)
    df = pd.read_csv(obj['Body'])
    logging.info(f"Extracted data from S3 bucket: {bucket_name}, file: {file_key}")
    return df

def extract_from_db(connection_string, query):
    # Extract data from a database
    engine = create_engine(connection_string)
    df = pd.read_sql(query, engine)
    logging.info("Extracted data from database.")
    return df

# ------------------- Transformation Functions -------------------
def validate_columns(df, required_columns):
    # Ensure required columns are present in the dataset
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    logging.info("Validated required columns.")

def handle_missing_values(df, strategy='mean', columns=None):
    # Handle missing values based on the strategy (mean, median, mode or remove)
    if columns is None:
        columns = df.columns
    for col in columns:
        if strategy == 'mean':
            df[col] = df[col].fillna(df[col].mean())
        elif strategy == 'median':
            df[col] = df[col].fillna(df[col].median())
        elif strategy == 'mode':
            df[col] = df[col].fillna(df[col].mode()[0])
        elif strategy =='remove':
            df[col] = df[col].dropna()
        else:
            raise ValueError("Invalid strategy. Use 'mean', 'median', 'mode' or 'remove.")
    logging.info("Handled missing values.")
    return df

def standardize_column_names(df):
    # Standardize column names to lowercase and replace spaces with underscores
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    logging.info("Standardized column names.")
    return df

def date_separator(df):
    # Handle inconsistent date seperators
    df['date'] = df['date'].str.replace('/', '-')
    logging.info("Date separator consistent.")
    return df

# def dates_to_datetime(df):
#     # Convert date columns from string to datetime
#     df['date'] = pd.to_datetime(df['date'])
#     logging.info("Converted date columns to datetime.")
#     return df

def remove_outliers(df):
    # Remove outliers from the dataset
    # The nature of this dataset means that there should be no sales greater than £1000
    df = df[df['sales']<= 1500]
    logging.info("Removed outliers.")
    return df

def remove_duplicates(df):
    # Remove duplicate rows from the dataset
    initial_count = len(df)
    df = df.drop_duplicates()
    final_count = len(df)
    logging.info(f"Removed {initial_count - final_count} duplicate rows.")
    return df

def convert_data_types(df, column_type_mapping):
    # Convert columns to specified data types
    for column, dtype in column_type_mapping.items():
        df[column] = df[column].astype(dtype)
    logging.info("Converted data types.")
    return df

# ------------------- Loading Functions -------------------
def load_to_db(df, connection_string, table_name):
    # Load data into a database
    engine = create_engine(connection_string)
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    logging.info(f"Loaded data to database table: {table_name}")
    #load_to_db(data, 'sqlite:///my_database.db', 'cleaned_data')

def load_to_csv(df, file_path):
    # Save the data to a CSV file
    df.to_csv(file_path, index=False)
    logging.info(f"Data saved to CSV file: {file_path}")
    #load_to_csv(data, 'cleaned_data.csv')
    

def load_to_s3(df, bucket_name, file_key):
    # Load the data to an S3 bucket
    s3 = boto3.client('s3')
    csv_buffer = df.to_csv(index=False)
    s3.put_object(Bucket=bucket_name, Key=file_key, Body=csv_buffer)
    logging.info(f"Loaded data to S3 bucket: {bucket_name}, file: {file_key}")
    
def load_to_rds(df):
    # Load variables from .env file
    load_dotenv()

    # Database connection details
    db_host =  os.getenv('db_host') 
    db_name = 'mysql'
    db_user = os.getenv('db_username')  
    db_password = os.getenv('db_password') 

    # Create a connection to RDS

    connection_string = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}'
    engine = create_engine(connection_string)

    with engine.connect() as connection:
        #print("Connection successful!")
    
        with connection.connection.cursor() as cursor:
            # SQL to create a database
            query = "CREATE DATABASE IF NOT EXISTS sales;"
            cursor.execute(query)
            #print("Database 'sales' created successfully!")
        
    # Update connection string to point to the new database
    sales_connection_string = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/sales'
    sales_engine = create_engine(sales_connection_string)

    # Load transformed data into the new database
    df.to_sql('sales_data', con=sales_engine, if_exists='replace', index=False)
    #print("Data loaded into the 'sales_data' table successfully!")

# ------------------- Main ETL Function -------------------
def etl_pipeline():
    # Run the ETL pipeline
    # Extraction
    try:
        data = extract_csv_from_s3('tungstennn-bucket', 'messy_raw_data.csv')
    except Exception as e:
        logging.error(f"Extraction failed: {e}")
        return

    # Transformation
    try:
        validate_columns(data, ['date', 'category', 'sales', 'region'])
        data = handle_missing_values(data, strategy='remove', columns=['sales'])
        data = standardize_column_names(data)
        #data = remove_duplicates(data)
        data = convert_data_types(data, {'sales': 'float'})
    except Exception as e:
        logging.error(f"Transformation failed: {e}")
        return

    # Loading
    try:
        load_to_rds(data)
    except Exception as e:
        logging.error(f"Loading failed: {e}")
        return

    logging.info("ETL pipeline completed successfully.")

# ------------------- Run the Pipeline -------------------
if __name__ == "__main__":
    etl_pipeline()
