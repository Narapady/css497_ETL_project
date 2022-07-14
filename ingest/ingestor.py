import os
from dotenv import load_dotenv
from s3 import S3AWS 

class Ingestor:
    """
    Ingestor class is repsonsible for ingesting data from source system with
    instance method ingest_data() to asw object stroage s3. The instantiation take
    source to ingest data from, aws s3 object, and the name of s3 bucket to store the data.

    """
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

    def __init__(self, source: str, bucket_name: str, s3: S3AWS):
        self.source = source
        self.bucket_name = bucket_name
        self.s3 = s3
    
    def ingest_data(self) -> None:
        """
        Executiong ingesting or extracting data to s3 bucket based on name of the source
        passed in the instantiation. 
        """
        if self.source == "kaggle":
            self.s3.ingest_from_kaggle(self.kaggle_sources, self.bucket_name)
        elif self.source == "usda":
            self.s3.ingest_from_usda(self.usda_sources, self.bucket_name)

def aws_credentials() -> None:
    """
    load aws s3 credentials to gain access to S3 
    """
    load_dotenv()

def main() -> None:
    """
    Main function of ingestion program. One aws s3 is instantiated, and
    ingest data from 2 sources systems including data from usda and kaggle. 
    Data will land in S3 with specified bucket names. 
    """
    aws_credentials() 
    
    s3 = S3AWS(os.getenv("ACCESS_KEY_ID"),os.getenv("SECRET_ACCESS_KEY"))

    ingestor_kaggle = Ingestor("kaggle", "s3-bucket-raw-kaggle", s3)
    ingestor_kaggle.ingest_data()

    ingestor_usda = Ingestor("usda", "s3-bucket-raw-usda", s3)
    ingestor_usda.ingest_data()

if __name__ == "__main__":
    main()













