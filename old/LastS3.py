import boto3

def get_last_added_file(bucket_name, folder_path):
    s3 = boto3.client('s3')

    # List objects in the bucket within the specified folder path
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_path)

    # Filter objects to exclude subfolders
    objects = [obj for obj in response['Contents'] if not obj['Key'].endswith('/')]

    if not objects:
        return None

    # Sort objects based on LastModified timestamp in descending order
    sorted_objects = sorted(objects, key=lambda obj: obj['LastModified'], reverse=True)

    # Retrieve the key (file path) of the last added file
    last_added_key = sorted_objects[0]['Key']

    return last_added_key

# Usage example
bucket_name = 'your-bucket-name'
folder_path = 'path/to/folder/'

last_added_file = get_last_added_file(bucket_name, folder_path)

if last_added_file:
    # Print the key (file path) of the last added file
    print(last_added_file)
else:
    print("No files found in the specified folder.")
    
