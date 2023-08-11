import boto3

def add_update_column(table_name, unique_key, column_name, column_value):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    response = table.update_item(
        Key={ 'unique_key_name': unique_key },  # Replace 'unique_key_name' with the actual unique key attribute name
        UpdateExpression=f"set {column_name} = :value",  # Replace 'column_name' with the actual column name
        ExpressionAttributeValues={ ":value": column_value }
    )
    
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print(f"Successfully added/updated column '{column_name}' for row with unique key '{unique_key}'")
    else:
        print("Failed to add/update column")

# Example usage
add_update_column('YourTableName', 'unique_key_value', 'column_name', 'column_value')
