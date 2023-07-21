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
