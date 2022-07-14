import requests
import os
import boto3
import zipfile
from typing import Optional
import util

class S3AWS:
    def __init__(self, access_key_id: Optional[str], secret_access_key: Optional[str]):
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.bucket_list = []

    def create_bucket(self, bucket_name: str):
        client = boto3.client('s3', 
                           aws_access_key_id=self.access_key_id,
                           aws_secret_access_key=self.secret_access_key)
        client.create_bucket(Bucket=bucket_name)
        self.bucket_list.append(bucket_name)

        return client

    def list_all_buckets(self):
        client = boto3.client('s3', 
                           aws_access_key_id=self.access_key_id,
                           aws_secret_access_key=self.secret_access_key)
        print(client.list_buckets())

    def ingest_from_usda(self, sources: list[str], bucket_name: str) -> None:
        source_list = [util.get_links(source) for source in sources]
        s3 = self.create_bucket(bucket_name=bucket_name) 

        for urls_dict in source_list: 
            for key, values in urls_dict.items():
                key = util.to_lowercase(key)        
                for link in values:
                    req = requests.get(link)
                    filename = req.url[link.rfind("/") + 1: link.rfind("?")]
                    s3.put_object( 
                        Bucket= bucket_name,
                        Body= req.content,
                        Key=  key + "/" + filename
                    )    

    def ingest_from_kaggle(self, sources: list[str], bucket_name: str) -> None:
        s3 = self.create_bucket(bucket_name) 
        for api_command in sources:
            os.system(api_command)
            filename = api_command.split("/")[1]
            with zipfile.ZipFile(filename + ".zip") as zip:
                zip.extractall()
                for file in os.listdir():
                    if ".csv" in file:
                        s3.upload_file(file, bucket_name, "obesity/" + file)
                
        os.system("rm *.zip *.csv")

