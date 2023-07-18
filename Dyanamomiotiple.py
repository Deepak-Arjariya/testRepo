import boto3

# Configure AWS credentials and region
session = boto3.Session(
    aws_access_key_id='YOUR_ACCESS_KEY',
    aws_secret_access_key='YOUR_SECRET_KEY',
    region_name='us-west-2'  # replace with your desired region
)

# Create DynamoDB client
dynamodb = session.client('dynamodb')

# Define query parameters
table_name = 'YourTableName'
column_name = 'YourColumnName'
desired_values = ['Value1', 'Value2', 'Value3']  # Add your desired values here

# Construct the keys for BatchGetItem
keys = [{'YourColumnName': {'S': value}} for value in desired_values]

# Construct the BatchGetItem request
response = dynamodb.batch_get_item(
    RequestItems={
        table_name: {
            'Keys': keys
        }
    }
)

# Retrieve the queried items
items = response['Responses'][table_name]

# Process the queried items
for item in items:
    print(item)
