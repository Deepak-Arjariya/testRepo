import boto3

# Create a DynamoDB client
dynamodb = boto3.client('dynamodb')

# Specify the table name
table_name = 'your-table-name'

# Specify the column name
column_name = 'your-column-name'

# Set to store unique values
unique_values = set()

# Scan the table to retrieve all items
response = dynamodb.scan(
    TableName=table_name
)

# Process the response and extract unique values from the column
for item in response['Items']:
    if column_name in item:
        value = item[column_name]
        value_type = list(value.keys())[0]
        value_data = value[value_type]
        unique_values.add(value_data)

# Print the unique values
print("Unique values in column:", unique_values)





import boto3

# Create a DynamoDB client
dynamodb = boto3.client('dynamodb')

# Specify the table name and GSI index name
table_name = 'your-table-name'
index_name = 'your-gsi-index-name'

# Specify the value for querying
category_value = 'your-category-value'

# Query using the GSI
response = dynamodb.query(
    TableName=table_name,
    IndexName=index_name,
    KeyConditionExpression='blr_category = :val',
    ExpressionAttributeValues={
        ':val': {'S': category_value}
    }
)

# Process the response
items = response['Items']
# Process the items retrieved from the query result





huwhyimport boto3

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
desired_value = 'YourDesiredValue'

# Construct the query
response = dynamodb.query(
    TableName=table_name,
    KeyConditionExpression="#col = :value",
    ExpressionAttributeNames={"#col": column_name},
    ExpressionAttributeValues={":value": {"S": desired_value}}
)

# Retrieve the queried items
items = response['Items']

# Process the queried items
for item in items:
    print(item)
    
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


import boto3

# Create DynamoDB client
dynamodb = boto3.client('dynamodb')

# Define query parameters
table_name = 'YourTableName'
column_name = 'YourColumnName'
desired_value = 'YourDesiredValue'

# Construct the scan parameters
scan_params = {
    'TableName': table_name,
    'FilterExpression': '#col = :value',
    'ExpressionAttributeNames': {'#col': column_name},
    'ExpressionAttributeValues': {':value': {'S': desired_value}}
}

# Perform the scan operation
response = dynamodb.scan(**scan_params)

# Retrieve the scanned items
items = response['Items']

# Process the scanned items
for item in items:
    print(item)
    






import boto3

# Create DynamoDB client
dynamodb = boto3.client('dynamodb')

# Define query parameters
table_name = 'YourTableName'
index_name = 'YourGSIName'
column_name = 'YourColumnName'
desired_value = 'YourDesiredValue'

# Construct the query parameters
query_params = {
    'TableName': table_name,
    'IndexName': index_name,
    'KeyConditionExpression': "#col = :value",
    'ExpressionAttributeNames': {'#col': column_name},
    'ExpressionAttributeValues': {':value': {'S': desired_value}}
}

# Perform the query operation
response = dynamodb.query(**query_params)

# Retrieve the queried items
items = response['Items']

# Process the queried items
for item in items:
    print(item)




import boto3

# Create DynamoDB client
dynamodb = boto3.client('dynamodb')

# Define query parameters
table_name = 'YourTableName'
index_name = 'YourGSIName'
column_name = 'YourColumnName'
desired_value = 'YourDesiredValue'

# Construct the query parameters
query_params = {
    'TableName': table_name,
    'IndexName': index_name,
    'KeyConditionExpression': "#col = :value",
    'FilterExpression': "attribute_name = :attribute_value",
    'ExpressionAttributeNames': {'#col': column_name},
    'ExpressionAttributeValues': {
        ':value': {'S': desired_value},
        ':attribute_value': {'S': 'AdditionalFilterValue'}
    }
}

# Perform the query operation
response = dynamodb.query(**query_params)

# Retrieve the queried items
items = response['Items']

# Process the queried items
for item in items:
    print(item)
    
