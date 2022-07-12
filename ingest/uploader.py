import boto3
import os
from dotenv import load_dotenv


load_dotenv()

client = boto3.client('s3', 
                       aws_access_key_id=os.getenv("ACCESS_KEY_ID"),
                       aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"))
client.create_bucket(Bucket="s3-bucket-raw-usda-ers")

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
