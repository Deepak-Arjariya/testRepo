import boto3
import json

def lambda_handler(event, context):
    # Retrieve the query parameters from the event
    table_name = event['queryStringParameters']['table']
    index_name = event['queryStringParameters']['index']
    index_value = event['queryStringParameters']['value']
    limit = int(event['queryStringParameters'].get('limit', '10'))
    start_key = event['queryStringParameters'].get('startKey', None)

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
        'Limit': limit
    }

    if start_key:
        query_params['ExclusiveStartKey'] = start_key

    # Query DynamoDB
    response = dynamodb.query(**query_params)

    # Retrieve the items
    items = response['Items']

    # Check if there are more pages
    has_more_pages = 'LastEvaluatedKey' in response

    # Prepare the response
    response_payload = {
        'items': items,
        'hasMorePages': has_more_pages
    }

    return {
        'statusCode': 200,
        'body': json.dumps(response_payload)
    }
  }
