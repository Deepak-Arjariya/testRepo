import boto3

# Create a DynamoDB client
dynamodb = boto3.client('dynamodb')

# Define the query parameters
table_name = 'YourTableName'
index_name = 'blr_category'
key_condition_expression = 'blr_category = :category'
projection_expression = 'attribute1, attribute2'  # Adjust with the desired attributes
limit_per_page = 100  # Adjust the desired limit per page

# Define the attribute values for the query
expression_attribute_values = {
    ':category': {'S': 'YourCategoryValue'}  # Adjust with the desired category value
}

# Construct the query parameters
query_params = {
    'TableName': table_name,
    'IndexName': index_name,
    'KeyConditionExpression': key_condition_expression,
    'ProjectionExpression': projection_expression,
    'Limit': limit_per_page,
    'ExpressionAttributeValues': expression_attribute_values
}

# Execute the query
response = dynamodb.query(**query_params)

# Process the items from the current page
items = response['Items']
for item in items:
    # Process each item as needed
    print(item)
  
