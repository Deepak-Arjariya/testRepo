import boto3

def create_last_evaluated_key_table(table_name, gsi_table_name):
    dynamodb = boto3.resource('dynamodb')
    
    # Create the table to store last evaluated keys
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'QueryId',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'QueryId',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    
    # Wait for the table to be created
    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
    
    # Add the GSI table reference to the new table
    gsi_table = dynamodb.Table(gsi_table_name)
    gsi_arn = gsi_table.table_arn
    table.update(
        AttributeDefinitions=[
            {
                'AttributeName': 'QueryId',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'LastEvaluatedKey',
                'AttributeType': 'S'
            }
        ],
        GlobalSecondaryIndexUpdates=[
            {
                'Create': {
                    'IndexName': 'GsiTableReference',
                    'KeySchema': [
                        {
                            'AttributeName': 'QueryId',
                            'KeyType': 'HASH'
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    },
                    'TableArn': gsi_arn
                }
            }
        ]
    )
    
    # Fill the table with values from BBPS biller table
    bbps_table = dynamodb.Table('BBPSBillerTable')
    response = bbps_table.scan()
    items = response['Items']
    
    while 'LastEvaluatedKey' in response:
        last_key = response['LastEvaluatedKey']
        response = bbps_table.scan(ExclusiveStartKey=last_key)
        items.extend(response['Items'])
    
    # Update the new table with values from the BBPS biller table
    last_evaluated_table = dynamodb.Table(table_name)
    with last_evaluated_table.batch_writer() as batch:
        for item in items:
            query_id = item['QueryId']
            last_evaluated_key = item['LastEvaluatedKey']
            batch.put_item(Item={'QueryId': query_id, 'LastEvaluatedKey': last_evaluated_key})
    
    print(f"Last evaluated key table '{table_name}' filled successfully with values from BBPS biller table.")

# Example usage
table_name = 'LastEvaluatedKeys'
gsi_table_name = 'YourGsiTableName'
create_last_evaluated_key_table(table_name, gsi_table_name)
  
