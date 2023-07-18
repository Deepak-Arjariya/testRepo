import boto3

# Create a DynamoDB client
dynamodb = boto3.client('dynamodb')

# Define the table name and global secondary index name
table_name = 'YourTableName'
index_name = 'YourGSIName'

# Define the value you want to retrieve from the GSI
desired_value = 'YourDesiredValue'

# Create an empty list to store all items
all_items = []

# Paginate through the results
paginator = dynamodb.get_paginator('query')
iterator = paginator.paginate(
    TableName=table_name,
    IndexName=index_name,
    KeyConditionExpression='YourGSIKey = :value',
    ExpressionAttributeValues={
        ':value': {'S': desired_value}
    }
)

for page in iterator:
    items = page['Items']
    all_items.extend(items)

# Print all the retrieved items
for item in all_items:
    print(item)
