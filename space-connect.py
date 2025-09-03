#!./tensorflow/bin/python

# Step 1: Import the all necessary libraries and SDK commands.
import os
import boto3
import botocore
import sys
import json

if len(sys.argv) < 2:
    print("error: Must provide name of file in input.")
    sys.exit(1)

with open("password.json", "r") as file:
    data = json.load(file)

    print(data['aws_access_key_id'])
    print(data['aws_secret_access_key'])

    # Step 2: The new session validates your request and directs it to your Space's specified endpoint using the AWS SDK.
    session = boto3.session.Session()
    client = session.client('s3',
                            region_name='sfo3', # Use the region in your endpoint.
                            endpoint_url='https://sfo3.digitaloceanspaces.com', # Find your endpoint in the control panel, under Settings. Prepend "https://".
                            aws_access_key_id=data['aws_access_key_id'], # Access key pair. You can create access key pairs using the control panel or API.
                            aws_secret_access_key=data['aws_secret_access_key'])

    #client.create_bucket(Bucket='tcb-drone')

    print(str(client))
    # List all buckets on your account.
    response = client.list_buckets()
    spaces = [space['Name'] for space in response['Buckets']]
    print(str(response))

    # Step 3: Call the put_object command and specify the file to upload.
    client.put_object(Bucket='tcb-drone', # The path to the directory you want to upload the object to, starting with your Space name.
                      Key=str(sys.argv[1]), # Object key, referenced whenever you want to access this file later.
                      Body=b'Hello, World!', # The object's contents.
                      ACL='private', # Defines Access-control List (ACL) permissions, such as private or public.
                      Metadata={ # Defines metadata tags.
                          'x-amz-meta-my-key': 'your-value'
                      }
                    )
