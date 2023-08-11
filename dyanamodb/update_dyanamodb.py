import boto3

# Initialize the DynamoDB client
dynamodb = boto3.client('dynamodb')

# Specify the table name
table_name = 'YourTableName'

# Iterate through the DataFrame
for index, row in df.iterrows():
    partition_key_value = str(row['PartitionKeyColumn'])  # Assuming a partition key column in the DataFrame
    
    # Construct the UpdateExpression and ExpressionAttributeValues
    update_expression = "SET "
    expression_attribute_values = {}
    
    for column_name in df.columns:
        if column_name != 'PartitionKeyColumn':
            update_expression += f" {column_name} = :{column_name},"
            expression_attribute_values[f":{column_name}"] = {'S': str(row[column_name])}
    
    update_expression = update_expression.rstrip(',')
    
    # Update the item
    response = dynamodb.update_item(
        TableName=table_name,
        Key={
            'PartitionKey': {'S': partition_key_value}
        },
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values
    )
    
    print(f"Item with PartitionKey {partition_key_value} updated successfully!")







import boto3

# Initialize the DynamoDB client
dynamodb = boto3.client('dynamodb')

# Specify the table name
table_name = 'YourTableName'

# Iterate through the DataFrame
for index, row in df.iterrows():
    partition_key_value = str(row['PartitionKeyColumn'])  # Assuming a partition key column in the DataFrame
    
    # Delete the old item
    delete_response = dynamodb.delete_item(
        TableName=table_name,
        Key={
            'PartitionKey': {'S': partition_key_value}
        }
    )
    
    print(f"Old item with PartitionKey {partition_key_value} deleted successfully!")
    
    # Create a new item
    new_item = {
        'PartitionKey': {'S': partition_key_value}
    }
    
    for column_name in df.columns:
        if column_name != 'PartitionKeyColumn':
            # Clean the column name to remove special characters
            cleaned_column_name = column_name.replace("-", "_")  # Replace hyphens with underscores
            
            new_item[cleaned_column_name] = {'S': str(row[column_name])}
    
    # Insert the new item
    put_response = dynamodb.put_item(
        TableName=table_name,
        Item=new_item
    )
    
    print(f"New item with PartitionKey {partition_key_value} created successfully!")
    
