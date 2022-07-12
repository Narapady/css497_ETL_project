import boto3
import os
from aws_access_key import ACCESS_KEY_ID, SECRET_ACCESS_KEY

client = boto3.client('s3', aws_access_key_id= ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)
client.create_bucket(Bucket="first-s3-bucket-test")
# client = boto3.client('s3', aws_access_key_id= ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)

for filename in os.listdir():
    if ".xls" in filename:
        with open(filename, "rb") as file:
            key = "test-xsl/" + filename
            client.upload_fileobj(file,"first-s3-bucket-test", key)
