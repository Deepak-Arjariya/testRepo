import boto3

def get_last_added_file(bucket_name):
    s3 = boto3.client('s3')

    # List objects in the bucket
    response = s3.list_objects_v2(Bucket=bucket_name)

    # Sort objects based on LastModified timestamp in descending order
    sorted_objects = sorted(response['Contents'], key=lambda obj: obj['LastModified'], reverse=True)

    # Retrieve the key (file path) of the last added file
    last_added_key = sorted_objects[0]['Key']

    return last_added_key

# Usage example
bucket_name = 'your-bucket-name'

last_added_file = get_last_added_file(bucket_name)

# Print the key (file path) of the last added file
print(last_added_file)
