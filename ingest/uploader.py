import boto3
import os
from aws_access_key import ACCESS_KEY_ID, SECRET_ACCESS_KEY

client = boto3.client('s3', aws_access_key_id= ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)
client.create_bucket(Bucket="s3-bucket-raw-usda-ers")

for filename in os.listdir():
    if "xls" in filename:
        with open(filename, "rb") as file:
            key = "test-xsl/" + filename
            client.upload_fileobj(file,"s3-bucket-raw-usda-ers", key)

for dir in os.listdir():
    if "-" in dir:
        os.chdir(dir)
        for xls_file in os.listdir():
            with open(xls_file, "rb") as file:
                key = dir + "/" + xls_file
                client.upload_fileobj(file,"s3-bucket-raw-usda-ers", key)
        # go one level up a directory
        parent_path = os.path.dirname(os.getcwd())
        os.chdir(parent_path)
