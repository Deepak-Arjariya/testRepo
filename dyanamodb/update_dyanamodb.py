import boto3
import pandas as pd

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='your_region')

# Load Excel data
excel_file = 'your_excel_file.xlsx'
df = pd.read_excel(excel_file)
value_to_update = df['Column_Name'][0]  # Adjust 'Column_Name' to the actual column name

# Initialize DynamoDB table
table_name = 'YourTableName'
table = dynamodb.Table(table_name)

# Update the item in DynamoDB
response = table.update_item(
    Key={
        'PartitionKey': value_to_update  # Assuming your partition key attribute is named 'PartitionKey'
    },
    UpdateExpression='SET attribute_name = :new_value',  # Replace 'attribute_name' with your attribute
    ExpressionAttributeValues={
        ':new_value': 'new_value_here'
    }
)

print("Item updated:", response)
