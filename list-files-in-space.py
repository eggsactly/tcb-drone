#!./tensorflow/bin/python

# Step 1: Import the all necessary libraries and SDK commands.
import os
import boto3
import botocore
import sys
import json
import datetime

def human_readable_bytes(nbytes):
    """
    Converts a byte count into a human-readable string with appropriate suffixes.

    Args:
        nbytes (int): The number of bytes.

    Returns:
        str: A string representing the human-readable byte size.
    """
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    i = 0
    while nbytes >= 1024 and i < len(suffixes) - 1:
        nbytes /= 1024.0
        i += 1
    
    # Format the number to two decimal places, removing trailing zeros and the decimal point if not needed
    formatted_nbytes = f'{nbytes:.2f}'.rstrip('0').rstrip('.')
    return f'{formatted_nbytes} {suffixes[i]}'

with open("password.json", "r") as file:
    data = json.load(file)

    # Step 2: The new session validates your request and directs it to your Space's specified endpoint using the AWS SDK.
    session = boto3.session.Session()
    client = session.client('s3',
                            region_name='sfo3', # Use the region in your endpoint.
                            endpoint_url='https://sfo3.digitaloceanspaces.com', # Find your endpoint in the control panel, under Settings. Prepend "https://".
                            aws_access_key_id=data['aws_access_key_id'], # Access key pair. You can create access key pairs using the control panel or API.
                            aws_secret_access_key=data['aws_secret_access_key'])

    #client.create_bucket(Bucket='tcb-drone')

    #print(str(client))
    # List all buckets on your account.
    response = client.list_buckets()
    spaces = [space['Name'] for space in response['Buckets']]
    
    # Get the list of files 
    
    response = client.list_objects_v2(
        Bucket='tcb-drone',
        Delimiter=' ',
        EncodingType='url'
    )
    
    maxlen = 0
    for entry in response['Contents']:
        if maxlen < len(str(entry['Key'])):
            maxlen = len(str(entry['Key']))
    
    # We want to sort with respect to time 
    sorted_by_name_desc = sorted(response['Contents'], key=lambda x: x['LastModified'], reverse=False)
    
    # https://tcb-drone.sfo3.digitaloceanspaces.com/" + 
    
    print("File path:".ljust(maxlen + 1) + " Size:", file=sys.stderr)
    print("----------".ljust(maxlen + 1) + " -----", file=sys.stderr)
    for entry in sorted_by_name_desc:
        print((str(entry['Key'])).ljust(maxlen + 1) + " " + str(human_readable_bytes(entry['Size'])))

               
    sys.exit(0)

