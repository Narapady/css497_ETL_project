import boto3
import os
from dotenv import load_dotenv
from smart_open import smart_open
from typing import Optional
from dataclasses import dataclass
import pandas as pd
import numpy as np

@dataclass
class S3AWS:
    """
    S3AWS represents aws object storage s3. It handles necessary features including
    authenticating to access to s3, and creating bucket to store the ingested data
    """
    # def __init__(self, access_key_id: Optional[str], secret_access_key: Optional[str]):
    #     self.access_key_id = access_key_id
    #     self.secret_access_key = secret_access_key
    access_key_id: Optional[str] 
    secret_key_id: Optional[str]

    def create_bucket(self, bucket_name: str):
        """
        Create S3 bucket with bucket_name
        """
        client = boto3.client('s3', 
                           aws_access_key_id=self.access_key_id,
                           aws_secret_access_key=self.secret_key_id)
        client.create_bucket(Bucket=bucket_name)

        return client

    def load_df(self, bucket_name: str, key: str, type: str, sheet: int):
        path = f"s3://{self.access_key_id}:{self.secret_key_id}@{bucket_name}/{key}"
        
        if type == "csv":
            return pd.read_csv(smart_open(path))
        elif type == "xls":
            return pd.read_excel(path, sheet)

