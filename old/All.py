import boto3

# Create a DynamoDB client
dynamodb = boto3.client('dynamodb')

# Specify the table name
table_name = 'your-table-name'

# Specify the column name
column_name = 'your-column-name'

# List to store column values
column_values = []

# Perform initial scan operation
response = dynamodb.scan(
    TableName=table_name
)

# Process the response and extract column values
while 'Items' in response:
    for item in response['Items']:
        if column_name in item:
            value = item[column_name]
            value_type = list(value.keys())[0]
            value_data = value[value_type]
            column_values.append(value_data)

    # Check if there are more pages to scan
    if 'LastEvaluatedKey' in response:
        last_evaluated_key = response['LastEvaluatedKey']
        response = dynamodb.scan(
            TableName=table_name,
            ExclusiveStartKey=last_evaluated_key
        )
    else:
        break

# Print the column values
print("Values in column:", column_values)
