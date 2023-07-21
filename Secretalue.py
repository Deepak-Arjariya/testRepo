import boto3

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
        
        
