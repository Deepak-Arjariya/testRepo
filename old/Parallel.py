import boto3
import concurrent.futures

# Create a DynamoDB client
dynamodb = boto3.client('dynamodb')

# Define the query parameters
table_name = 'YourTableName'
index_name = 'index-gsi'
key_condition_expression = 'blr_category = :category'
projection_expression = 'attribute1, attribute2'  # Adjust with the desired attributes
limit_per_page = 100  # Adjust the desired limit per page

# Define the attribute values for the query
expression_attribute_values = {
    ':category': {'S': 'YourCategoryValue'}  # Adjust with the desired category value
}

# Variables for pagination
last_evaluated_key = None
items = []

def fetch_page(page_key):
    query_params = {
        'TableName': table_name,
        'IndexName': index_name,
        'KeyConditionExpression': key_condition_expression,
        'ProjectionExpression': projection_expression,
        'Limit': limit_per_page,
        'ExpressionAttributeValues': expression_attribute_values,
        'ExclusiveStartKey': page_key
    }
    response = dynamodb.query(**query_params)
    return response['Items']

# Fetch the first page of results
items.extend(fetch_page(last_evaluated_key))

# Fetch subsequent pages concurrently
with concurrent.futures.ThreadPoolExecutor() as executor:
    while last_evaluated_key:
        future_to_key = {executor.submit(fetch_page, last_evaluated_key): last_evaluated_key}
        for future in concurrent.futures.as_completed(future_to_key):
            page_key = future_to_key[future]
            try:
                page_items = future.result()
                items.extend(page_items)
                last_evaluated_key = page_items[-1].get('LastEvaluatedKey')
            except Exception as e:
                print(f'Error fetching page with key {page_key}: {e}')

# Process all retrieved items
for item in items:
    # Process each item as needed
    print(item)
