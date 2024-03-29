import boto3
import zipfile
import tempfile

def extract_logos_from_zip(s3_bucket, zip_key, extract_folder, dynamodb_table):
    s3 = boto3.client('s3')
    dynamodb = boto3.resource('dynamodb')

    # Create a temporary directory to extract the files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Download the ZIP file
        zip_path = f'{temp_dir}/logos.zip'
        s3.download_file(s3_bucket, zip_key, zip_path)

        # Extract the ZIP file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Upload the extracted logos to a folder within the same S3 bucket
        extracted_files = []
        for extracted_file in temp_dir.iterdir():
            if extracted_file.is_file():
                extracted_key = f'{extract_folder}/{extracted_file.name}'
                s3.upload_file(str(extracted_file), s3_bucket, extracted_key)
                extracted_files.append(extracted_key)

        # Save the extracted file paths to DynamoDB
        table = dynamodb.Table(dynamodb_table)
        for file_path in extracted_files:
            table.put_item(Item={'logo_path': file_path})

# Usage example
s3_bucket = 'your-s3-bucket'
zip_key = 'path/to/logos.zip'
extract_folder = 'extracted_logos'
dynamodb_table = 'your-dynamodb-table'

extract_logos_from_zip(s3_bucket, zip_key, extract_folder, dynamodb_table)
import boto3
import zipfile
import tempfile
import os

def extract_logos_from_zip(s3_bucket, zip_key, extract_folder):
    s3 = boto3.client('s3')

    # Create a temporary directory to extract the files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Download the ZIP file
        zip_path = f'{temp_dir}/logos.zip'
        s3.download_file(s3_bucket, zip_key, zip_path)

        # Extract the ZIP file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Upload the extracted logos to a folder within the same S3 bucket
        extracted_files = []
        for extracted_file in os.listdir(temp_dir):
            extracted_file_path = os.path.join(temp_dir, extracted_file)
            if os.path.isfile(extracted_file_path):
                extracted_key = f'{extract_folder}/{extracted_file}'
                s3.upload_file(extracted_file_path, s3_bucket, extracted_key)
                extracted_files.append(extracted_key)

    return extracted_files

# Usage example
s3_bucket = 'your-s3-bucket'
zip_key = 'path/to/logos.zip'
extract_folder = 'extracted_logos'

extracted_files = extract_logos_from_zip(s3_bucket, zip_key, extract_folder)

# Print the extracted file paths
print(extracted_files)


import boto3
import zipfile
import tempfile
import os

def extract_logos_from_zip(s3_bucket, zip_key, extract_folder):
    s3 = boto3.client('s3')

    # Create a temporary directory to extract the files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Download the ZIP file
        zip_path = f'{temp_dir}/logos.zip'
        s3.download_file(s3_bucket, zip_key, zip_path)

        # Extract the ZIP file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Extract all files to a subdirectory within the temporary directory
            zip_ref.extractall(f'{temp_dir}/extracted')

        # Upload the extracted logos to a folder within the same S3 bucket
        extracted_files = []
        for root, dirs, files in os.walk(f'{temp_dir}/extracted'):
            for file in files:
                extracted_file_path = os.path.join(root, file)
                if os.path.isfile(extracted_file_path):
                    # Extract the relative path from the temporary directory
                    relative_path = os.path.relpath(extracted_file_path, f'{temp_dir}/extracted')
                    extracted_key = f'{extract_folder}/{relative_path}'
                    s3.upload_file(extracted_file_path, s3_bucket, extracted_key)
                    extracted_files.append(extracted_key)

    return extracted_files

# Usage example
s3_bucket = 'your-s3-bucket'
zip_key = 'path/to/logos.zip'
extract_folder = 'extracted_logos'

extracted_files = extract_logos_from_zip(s3_bucket, zip_key, extract_folder)

# Print the extracted file paths
print(extracted_files)
