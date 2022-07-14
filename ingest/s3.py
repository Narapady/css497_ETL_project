import boto3
from typing import Optional

class S3AWS:
    """
    S3AWS represents aws object storage s3. It handles necessary features including
    authenticating to access to s3, and creating bucket to store the ingested data
    """
    def __init__(self, access_key_id: Optional[str], secret_access_key: Optional[str]):
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.bucket_list = []

    def create_bucket(self, bucket_name: str):
        """
        Create S3 bucket with bucket_name
        """
        client = boto3.client('s3', 
                           aws_access_key_id=self.access_key_id,
                           aws_secret_access_key=self.secret_access_key)
        client.create_bucket(Bucket=bucket_name)
        self.bucket_list.append(bucket_name)

        return client


