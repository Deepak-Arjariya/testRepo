inimport boto3

# Initialize the AWS Secrets Manager client
secrets_manager = boto3.client('secretsmanager')

def list_secrets():
    try:
        response = secrets_manager.list_secrets()
        secrets = response['SecretList']
        for secret in secrets:
            print(f"Secret Name: {secret['Name']}")
    except Exception as e:
        print(f"Error listing secrets: {e}")

def update_secret(secret_name):
    try:
        new_secret_value = getpass.getpass("Enter the new secret value: ")
        response = secrets_manager.update_secret(SecretId=secret_name, SecretString=new_secret_value)
        print(f"Secret updated successfully for {secret_name}")
    except Exception as e:
        print(f"Error updating secret: {e}")

if __name__ == "__main__":
    list_secrets()

    secret_name = input("Enter the name of the secret to update: ")
    update_secret(secret_name)





import boto3
import json

# Initialize the AWS Secrets Manager client
secrets_manager = boto3.client('secretsmanager')

def get_secret_string(secret_name):
    try:
        response = secrets_manager.get_secret_value(SecretId=secret_name)
        secret_data = response['SecretString']
        secret_dict = json.loads(secret_data)
        return secret_dict
    except Exception as e:
        print(f"Error retrieving secret: {e}")
        return None

if __name__ == "__main__":
    secret_name = input("Enter the name of the secret to retrieve: ")
    secret = get_secret_string(secret_name)
    if secret:
        print("Secret Retrieved:")
        print(secret)





import boto3

# Initialize the AWS Secrets Manager client
secrets_manager = boto3.client('secretsmanager')

def get_secret_string(secret_name):
    try:
        response = secrets_manager.get_secret_value(SecretId=secret_name)
        if 'SecretString' in response:
            secret_string = response['SecretString']
            return secret_string
        else:
            print(f"SecretString not found for secret: {secret_name}")
            return None
    except Exception as e:
        print(f"Error retrieving secret: {e}")
        return None

if __name__ == "__main__":
    secret_name = input("Enter the name of the secret to retrieve: ")
    secret = get_secret_string(secret_name)
    if secret:
        print("Secret Retrieved:")
        print(secret)



import random
import string

def generate_strong_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))

    # Randomly replace some characters with uppercase characters
    num_uppercase = random.randint(1, length // 2)  # At least one, up to half of the password length
    uppercase_indices = random.sample(range(length), num_uppercase)
    password_list = list(password)
    for index in uppercase_indices:
        password_list[index] = password_list[index].upper()

    return ''.join(password_list)

if __name__ == "__main__":
    password_length = int(input("Enter the desired length of the password (default is 12): "))
    password = generate_strong_password(password_length)
    print("Generated Strong Password:", password)
    



import boto3
from datetime import datetime

# Initialize the AWS Secrets Manager client
secrets_manager = boto3.client('secretsmanager')

def update_secret_tag_with_timestamp(secret_name):
    try:
        response = secrets_manager.describe_secret(SecretId=secret_name)
        existing_tags = response['Tags']

        # Check if 'LastUpdated' tag already exists and remove it to update it later
        updated_tags = [tag for tag in existing_tags if tag['Key'] != 'LastUpdated']

        current_time = datetime.now().isoformat()
        updated_tags.append({
            'Key': 'LastUpdated',
            'Value': current_time
        })

        # Update the secret's tags
        secrets_manager.tag_resource(SecretId=secret_name, Tags=updated_tags)

        print(f"Tag 'LastUpdated' updated successfully for secret: {secret_name}")
    except Exception as e:
        print(f"Error updating tag: {e}")

if __name__ == "__main__":
    secret_name = input("Enter the name of the secret to update the tag: ")
    update_secret_tag_with_timestamp(secret_name)






import boto3

def send_email(subject, body, sender, recipient):
    ses_client = boto3.client('ses')
    
    response = ses_client.send_email(
        Source=sender,
        Destination={
            'ToAddresses': [recipient]
        },
        Message={
            'Subject': {
                'Data': subject
            },
            'Body': {
                'Text': {
                    'Data': body
                }
            }
        }
    )
    
    print("Email sent successfully:", response)

def lambda_handler(event, context):
    # Replace with your email addresses
    sender_email = "your_sender_email@example.com"
    recipient_email = "recipient@example.com"
    
    email_subject = "Test Email from AWS Lambda"
    email_body = "This is a test email sent from an AWS Lambda function."
    
    send_email(email_subject, email_body, sender_email, recipient_email)
    


import boto3
import logging

def send_email(subject, body, sender, recipient):
    ses_client = boto3.client('ses')
    
    try:
        response = ses_client.send_email(
            Source=sender,
            Destination={
                'ToAddresses': [recipient]
            },
            Message={
                'Subject': {
                    'Data': subject
                },
                'Body': {
                    'Text': {
                        'Data': body
                    }
                }
            }
        )
        
        logging.info("Email sent successfully: %s", response)
        return True

    except Exception as e:
        logging.error("Error sending email: %s", e)
        return False

def lambda_handler(event, context):
    # Replace with your email addresses
    sender_email = "your_sender_email@example.com"
    recipient_email = "recipient@example.com"
    
    email_subject = "Test Email from AWS Lambda"
    email_body = "This is a test email sent from an AWS Lambda function."
    
    if send_email(email_subject, email_body, sender_email, recipient_email):
        return {
            'statusCode': 200,
            'body': 'Email sent successfully!'
        }
    else:
        return {
            'statusCode': 500,
            'body': 'Failed to send email. Please check the logs for more details.'
        }


import boto3

# Initialize the AWS Organizations client
organizations_client = boto3.client('organizations')

def get_aws_account_name():
    try:
        response = organizations_client.describe_account()
        account_name = response['Account']['Name']
        return account_name
    except Exception as e:
        print(f"Error retrieving account name: {e}")
        return None

if __name__ == "__main__":
    account_name = get_aws_account_name()
    if account_name:
        print("AWS Account Name:", account_name)
    else:
        print("Unable to retrieve AWS account name.")




import boto3

# Initialize the AWS STS client
sts_client = boto3.client('sts')

def get_aws_account_name():
    try:
        # Get the AWS account ID from the execution context of the Lambda function
        account_id = sts_client.get_caller_identity()["Account"]

        # Get the account alias using the account ID
        account_aliases = sts_client.list_account_aliases()['AccountAliases']
        if account_aliases:
            account_name = account_aliases[0]
        else:
            # If there is no account alias, use the account ID as the name
            account_name = account_id

        return account_name

    except Exception as e:
        print(f"Error retrieving account name: {e}")
        return None

def lambda_handler(event, context):
    account_name = get_aws_account_name()
    if account_name:
        print("AWS Account Name:", account_name)
    else:
        print("Unable to retrieve AWS account name.")

if __name__ == "__main__":
    lambda_handler(None, None)  # For testing purposes
    



import boto3

# Initialize the AWS SES client
ses_client = boto3.client('ses')

def send_email(subject, body, sender, recipient, cc_recipients=None):
    destination = {
        'ToAddresses': [recipient]
    }
    
    if cc_recipients:
        destination['CcAddresses'] = cc_recipients

    try:
        response = ses_client.send_email(
            Source=sender,
            Destination=destination,
            Message={
                'Subject': {
                    'Data': subject
                },
                'Body': {
                    'Text': {
                        'Data': body
                    }
                }
            }
        )
        
        print("Email sent successfully:", response)
        return True

    except Exception as e:
        print("Error sending email:", e)
        return False

def lambda_handler(event, context):
    # Replace with your email addresses
    sender_email = "your_sender_email@example.com"
    recipient_email = "recipient@example.com"
    cc_recipients = ["cc_recipient1@example.com", "cc_recipient2@example.com"]

    email_subject = "Test Email from AWS Lambda"
    email_body = "This is a test email sent from an AWS Lambda function."

    if send_email(email_subject, email_body, sender_email, recipient_email, cc_recipients):
        return {
            'statusCode': 200,
            'body': 'Email sent successfully!'
        }
    else:
        return {
            'statusCode': 500,
            'body': 'Failed to send email. Please check the logs for more details.'
        }
        
