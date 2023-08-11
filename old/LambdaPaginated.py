import boto3
import json

def lambda_handler(event, context):
    # Retrieve the query parameters from the event
    table_name = event['queryStringParameters']['table']
    index_name = event['queryStringParameters']['index']
    index_value = event['queryStringParameters']['value']
    page = int(event['queryStringParameters'].get('page', '1'))
    items_per_page = 300

    # Calculate the starting item index based on the page number
    start_index = (page - 1) * items_per_page

    # Create a DynamoDB client
    dynamodb = boto3.client('dynamodb')

    # Prepare the query parameters
    query_params = {
        'TableName': table_name,
        'IndexName': index_name,
        'KeyConditionExpression': '#index = :value',
        'ExpressionAttributeNames': {
            '#index': index_name
        },
        'ExpressionAttributeValues': {
            ':value': {'S': index_value}
        },
        'Limit': items_per_page,
        'ScanIndexForward': True
    }

    # Query DynamoDB
    response = dynamodb.query(**query_params)

    # Retrieve the items for the requested page
    items = response['Items'][start_index:start_index+items_per_page]

    # Prepare the response
    response_payload = {
        'items': items
    }

    return {
        'statusCode': 200,
        'body': json.dumps(response_payload)
    }
  
