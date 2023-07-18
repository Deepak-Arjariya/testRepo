import boto3

def get_items_for_page(page_number):
    dynamodb = boto3.client('dynamodb')

    page_table_name = 'PageTable'
    page_table_key = str(page_number)  # Convert page number to string

    table_name = 'YourTableName'
    index_name = 'index-gsi'
    key_condition_expression = 'blr_category = :category'
    projection_expression = 'attribute1, attribute2'  # Adjust with the desired attributes
    limit_per_page = 100  # Adjust the desired limit per page

    expression_attribute_values = {
        ':category': {'S': 'YourCategoryValue'}  # Adjust with the desired category value
    }

    # Retrieve the LastEvaluatedKey for the desired page from PageTable
    dynamodb_resource = boto3.resource('dynamodb')
    page_table = dynamodb_resource.Table(page_table_name)
    response = page_table.get_item(Key={'PageNumber': page_table_key})
    last_evaluated_key = response.get('Item', {}).get('LastEvaluatedKey')

    items = []

    # Fetch pages until reaching the desired page or no more pages available
    while True:
        query_params = {
            'TableName': table_name,
            'IndexName': index_name,
            'KeyConditionExpression': key_condition_expression,
            'ProjectionExpression': projection_expression,
            'Limit': limit_per_page,
            'ExpressionAttributeValues': expression_attribute_values,
            'ExclusiveStartKey': last_evaluated_key
        }

        response = dynamodb.query(**query_params)
        items.extend(response['Items'])
        last_evaluated_key = response.get('LastEvaluatedKey')

        if not last_evaluated_key or len(items) >= limit_per_page * page_number:
            break

    # Store the LastEvaluatedKey in PageTable for future use
    page_table.put_item(Item={'PageNumber': page_table_key, 'LastEvaluatedKey': last_evaluated_key})

    # Return the items for the desired page
    start_index = limit_per_page * (page_number - 1)
    end_index = limit_per_page * page_number
    return items[start_index:end_index]

