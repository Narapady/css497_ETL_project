import os
import requests
import util
import zipfile
from dotenv import load_dotenv
from typing import Callable
from dataclasses import dataclass, field
from s3 import S3AWS 

def ingest_usda(sources: list[str], bucket_name: str, s3aws: S3AWS) -> None:
    """
    Ingest data from USDA ERS to specified S3 buckets. 'sources' paramenter
    is the website links that contain data to ingest. 
    """
    source_list = [util.get_links(source) for source in sources]
    s3 = s3aws.create_bucket(bucket_name=bucket_name) 

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

def ingest_kaggle(sources: list[str], bucket_name: str, s3aws: S3AWS) -> None:
    """
    Ingest data from Kaggle to specified S3 bucket via Kaggle API commnads.
    'sources' paramenter is a list of kaggle api commands to get the data. 
    """
    s3 = s3aws.create_bucket(bucket_name) 
    for api_command in sources:
        os.system(api_command)
        filename = api_command.split("/")[1]
        with zipfile.ZipFile(filename + ".zip") as zip:
            zip.extractall()
            for file in os.listdir():
                if ".csv" in file:
                    s3.upload_file(file, bucket_name, "obesity/" + file)
            
    os.system("rm *.zip *.csv")

def aws_credentials() -> None:
    """
    load aws s3 credentials to gain access to S3 
    """
    load_dotenv()

"""
Type alias for ingesting stragegy. Any callable object of this
type can be bass as parameter to Ingestor.ingest() method
"""
ingestStrategy = Callable[[list[str], str, S3AWS], None]

@dataclass
class Ingestor:
    """
    Ingestor class is repsonsible for ingesting data from source system with
    instance method ingest() to ingest data from source systems to asw object stroage s3.
    The instantiation takes s3 object, s3's bucket name to load data to, and list of source links/api commands
    """
    s3: S3AWS
    bucket_name: str
    sources: list[str] = field(default_factory=list[str]) 
    
    def ingest(self, ingest_strategy: ingestStrategy) -> None:
        """
        ingesting data to s3 bucket based on ingesting strategy
        """
        ingest_strategy(self.sources, self.bucket_name, self.s3)

def main() -> None:
    """
    Main function of ingestion program. One aws s3 is instantiated, and
    ingest data from 2 sources systems including data from usda and kaggle. 
    Data will land in S3 with specified bucket names. 
    """
    aws_credentials() 
    
    kaggle_sources = ["kaggle datasets download -d amanarora/obesity-among-adults-by-country-19752016",
                      "kaggle datasets download -d annedunn/obesity-and-gdp-rates-from-50-states-in-20142017",
                      "kaggle datasets download -d spittman1248/cdc-data-nutrition-physical-activity-obesity"
    ]   

    usda_sources = [
        "https://www.ers.usda.gov/data-products/commodity-consumption-by-population-characteristics/",
        "https://www.ers.usda.gov/data-products/food-availability-per-capita-data-system/",
        "https://www.ers.usda.gov/data-products/food-consumption-and-nutrient-intakes/",
        "https://www.ers.usda.gov/data-products/eating-and-health-module-atus/",
        "https://www.ers.usda.gov/data-products/food-price-outlook/",
        "https://www.ers.usda.gov/data-products/food-expenditure-series/"
    ]
    
    s3 = S3AWS(os.getenv("ACCESS_KEY_ID"),os.getenv("SECRET_ACCESS_KEY"))

    ingestor_kaggle = Ingestor(s3, "s3-bucket-raw-kaggle", kaggle_sources)
    ingestor_kaggle.ingest(ingest_kaggle)

    ingestor_usda = Ingestor(s3, "s3-bucket-raw-usda", usda_sources)
    ingestor_usda.ingest(ingest_usda)

# main program
if __name__ == "__main__":
    main()











