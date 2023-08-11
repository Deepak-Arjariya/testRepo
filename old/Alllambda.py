import boto3
import json

def lambda_handler(event, context):
    # Retrieve the query parameters from the event
    table_name = event['queryStringParameters']['table']

    # Create a DynamoDB client
    dynamodb = boto3.client('dynamodb')

    # Prepare the scan parameters
    scan_params = {
        'TableName': table_name
    }

    # Scan DynamoDB
    response = dynamodb.scan(**scan_params)

    # Retrieve all items
    items = response['Items']

    # Paginate if there are more items
    while 'LastEvaluatedKey' in response:
        scan_params['ExclusiveStartKey'] = response['LastEvaluatedKey']
        response = dynamodb.scan(**scan_params)
        items.extend(response['Items'])

    # Prepare the response
    response_payload = {
        'items': items
    }

    return {
        'statusCode': 200,
        'body': json.dumps(response_payload)
    }
}
