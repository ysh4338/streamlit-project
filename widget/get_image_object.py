import io
import boto3

import requests
from PIL import Image


def get_token():
    url = "http://169.254.169.254/latest/api/token"
    headers = {"X-aws-ec2-metadata-token-ttl-seconds": "3600"}
    response = requests.put(url, headers=headers)
    return response.text

def get_instance_metadata(token, endpoint):
    url = f"http://169.254.169.254/latest/meta-data/{endpoint}"
    headers = {"X-aws-ec2-metadata-token": token}
    response = requests.get(url, headers=headers)
    return response.text
    
def get_account_id(token):
    url = "http://169.254.169.254/latest/dynamic/instance-identity/document"
    headers = {"X-aws-ec2-metadata-token": token}
    response = requests.get(url, headers=headers)
    res = response.json()
    return res.get('accountId')


def get_s3_image():
    token = get_token()
    region = get_instance_metadata(token, "placement/region")
    
    accountId = get_account_id(token)
    bucket_name = f"lab-edu-bucket-image-{accountId}"
    
    object_key = "cj-olivenetworks.png"
    
    s3 = boto3.client('s3', region_name=region)
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    return Image.open(io.BytesIO(response['Body'].read()))