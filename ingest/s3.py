import boto3
import os
from dotenv import load_dotenv
from smart_open import smart_open
from typing import Optional
import pandas as pd
import numpy as np

class S3AWS:
    """
    S3AWS represents aws object storage s3. It handles necessary features including
    authenticating to access to s3, and creating bucket to store the ingested data
    """
    def __init__(self, access_key_id: Optional[str], secret_key_id: Optional[str]):
        self.access_key_id = access_key_id
        self.secret_key_id = secret_key_id

    def create_bucket(self, bucket_name: str):
        """
        Create S3 bucket with bucket_name
        """
        client = boto3.client('s3', 
                           aws_access_key_id=self.access_key_id,
                           aws_secret_access_key=self.secret_key_id)
        client.create_bucket(Bucket=bucket_name)

        return client

    def load_df(self, bucket_name: str, key: str, type: str, sheet: int) -> pd.DataFrame:
        path = f"s3://{self.access_key_id}:{self.secret_key_id}@{bucket_name}/{key}"
        if type == "csv":
            return pd.read_csv(smart_open(path))
        elif type == "xls":
            return pd.read_excel(smart_open(path), sheet)

        
    def df_to_s3(self, dataframe: pd.DataFrame, bucket_name: str, key: str, ) -> None:
        s3_bucket = self.create_bucket(bucket_name)
        if s3_bucket:
            s3_bucket.put_object(Bucket=bucket_name, Body=dataframe.to_csv(None).encode(), Key=key)
