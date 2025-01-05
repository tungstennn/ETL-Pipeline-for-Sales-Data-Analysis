import pandas as pd
import boto3
from sqlalchemy import create_engine
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ------------------- Extraction Functions -------------------
def extract_csv_from_s3(bucket_name, file_key):
    """Extract CSV file from S3 bucket."""
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket_name, Key=file_key)
    df = pd.read_csv(obj['Body'])
    logging.info(f"Extracted data from S3 bucket: {bucket_name}, file: {file_key}")
    return df

def extract_from_db(connection_string, query):
    """Extract data from a database."""
    engine = create_engine(connection_string)
    df = pd.read_sql(query, engine)
    logging.info("Extracted data from database.")
    return df

# ------------------- Transformation Functions -------------------
def validate_columns(df, required_columns):
    """Ensure required columns are present in the dataset."""
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    logging.info("Validated required columns.")

def handle_missing_values(df, strategy='mean', columns=None):
    """Handle missing values based on the strategy (mean, median, or mode)."""
    if columns is None:
        columns = df.columns
    for col in columns:
        if strategy == 'mean':
            df[col] = df[col].fillna(df[col].mean())
        elif strategy == 'median':
            df[col] = df[col].fillna(df[col].median())
        elif strategy == 'mode':
            df[col] = df[col].fillna(df[col].mode()[0])
        else:
            raise ValueError("Invalid strategy. Use 'mean', 'median', or 'mode'.")
    logging.info("Handled missing values.")
    return df

def standardize_column_names(df):
    """Standardize column names to lowercase and replace spaces with underscores."""
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    logging.info("Standardized column names.")
    return df

def remove_duplicates(df):
    """Remove duplicate rows from the dataset."""
    initial_count = len(df)
    df = df.drop_duplicates()
    final_count = len(df)
    logging.info(f"Removed {initial_count - final_count} duplicate rows.")
    return df

def convert_data_types(df, column_type_mapping):
    """Convert columns to specified data types."""
    for column, dtype in column_type_mapping.items():
        df[column] = df[column].astype(dtype)
    logging.info("Converted data types.")
    return df

# ------------------- Loading Functions -------------------
def load_to_db(df, connection_string, table_name):
    """Load data into a database."""
    engine = create_engine(connection_string)
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    logging.info(f"Loaded data to database table: {table_name}")

def load_to_csv(df, file_path):
    """Save the data to a CSV file."""
    df.to_csv(file_path, index=False)
    logging.info(f"Data saved to CSV file: {file_path}")

def load_to_s3(df, bucket_name, file_key):
    """Load the data to an S3 bucket."""
    s3 = boto3.client('s3')
    csv_buffer = df.to_csv(index=False)
    s3.put_object(Bucket=bucket_name, Key=file_key, Body=csv_buffer)
    logging.info(f"Loaded data to S3 bucket: {bucket_name}, file: {file_key}")

# ------------------- Main ETL Function -------------------
def etl_pipeline():
    """Run the ETL pipeline."""
    # Extraction
    try:
        data = extract_csv_from_s3('tungstennn-bucket', 'messy_raw_data.csv')
    except Exception as e:
        logging.error(f"Extraction failed: {e}")
        return

    # Transformation
    try:
        validate_columns(data, ['date', 'category', 'sales', 'region'])
        data = handle_missing_values(data, strategy='mean', columns=['sales'])
        data = standardize_column_names(data)
        data = remove_duplicates(data)
        data = convert_data_types(data, {'sales': 'float'})
    except Exception as e:
        logging.error(f"Transformation failed: {e}")
        return

    # Loading
    try:
        load_to_db(data, 'sqlite:///my_database.db', 'cleaned_data')
        load_to_csv(data, 'cleaned_data.csv')
    except Exception as e:
        logging.error(f"Loading failed: {e}")
        return

    logging.info("ETL pipeline completed successfully.")

# ------------------- Run the Pipeline -------------------
if __name__ == "__main__":
    etl_pipeline()
