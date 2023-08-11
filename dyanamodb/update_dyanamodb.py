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






import boto3

# Initialize the DynamoDB client
dynamodb = boto3.client('dynamodb')

# Specify the table name
table_name = 'YourTableName'

# Iterate through the DataFrame
for index, row in df.iterrows():
    partition_key_value = str(row['PartitionKeyColumn'])  # Assuming a partition key column in the DataFrame
    
    # Retrieve the existing item from DynamoDB
    existing_item = dynamodb.get_item(
        TableName=table_name,
        Key={
            'PartitionKey': {'S': partition_key_value}
        }
    )['Item']
    
    # Construct a set of attributes to remove
    attributes_to_remove = set(existing_item.keys()) - {'PartitionKey'}
    
    # Construct the UpdateExpression and ExpressionAttributeValues
    update_expression = "SET "
    expression_attribute_values = {}
    
    for column_name in df.columns:
        if column_name != 'PartitionKeyColumn':
            # Clean the column name to remove special characters
            cleaned_column_name = column_name.replace("-", "_")  # Replace hyphens with underscores
            
            update_expression += f" #{cleaned_column_name} = :{cleaned_column_name},"
            expression_attribute_values[f":{cleaned_column_name}"] = {'S': str(row[column_name])}
            attributes_to_remove.discard(cleaned_column_name)
    
    update_expression = update_expression.rstrip(',')
    
    # Construct the Remove expression for attributes to remove
    remove_expression = "REMOVE " + ", ".join(f"#{attr}" for attr in attributes_to_remove)
    
    # Update the item in DynamoDB
    response = dynamodb.update_item(
        TableName=table_name,
        Key={
            'PartitionKey': {'S': partition_key_value}
        },
        UpdateExpression=f"{update_expression} {remove_expression}",
        ExpressionAttributeValues=expression_attribute_values,
        ExpressionAttributeNames={
            f"#{cleaned_column_name}": column_name for column_name in df.columns if column_name != 'PartitionKeyColumn'
        }
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
    
    # Retrieve the existing item from DynamoDB
    existing_item = dynamodb.get_item(
        TableName=table_name,
        Key={
            'PartitionKey': {'S': partition_key_value}
        }
    ).get('Item', {})
    
    # Construct the UpdateExpression and ExpressionAttributeValues for attributes to update
    update_expression = "SET "
    expression_attribute_values = {}
    
    for column_name in df.columns:
        if column_name != 'PartitionKeyColumn':
            # Clean the column name to remove special characters
            cleaned_column_name = column_name.replace("-", "_")  # Replace hyphens with underscores
            
            # If the attribute exists in the existing item, update it
            if cleaned_column_name in existing_item:
                update_expression += f" #{cleaned_column_name} = :{cleaned_column_name},"
                expression_attribute_values[f":{cleaned_column_name}"] = {'S': str(row[column_name])}
            # If the attribute doesn't exist, add it
            else:
                update_expression += f" #{cleaned_column_name} = :{cleaned_column_name},"
                expression_attribute_values[f":{cleaned_column_name}"] = {'S': str(row[column_name])}
    
    update_expression = update_expression.rstrip(',')
    
    # Update the item in DynamoDB
    response = dynamodb.update_item(
        TableName=table_name,
        Key={
            'PartitionKey': {'S': partition_key_value}
        },
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ExpressionAttributeNames={
            f"#{cleaned_column_name}": column_name for column_name in df.columns if column_name != 'PartitionKeyColumn'
        }
    )
    
    print(f"Item with PartitionKey {partition_key_value} updated successfully!")
    
