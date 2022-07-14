import requests
import os
import boto3
import zipfile
from bs4 import BeautifulSoup
from dotenv import load_dotenv

def to_lowercase(word: str) -> str:
    result = word.split(" ")
    result = [item.lower() for item in result]
    return " ".join(result).replace(" ", "-")

def get_links(url: str) -> dict[str, list[str]]: 
    """
    Fetch the download links and group titles for each dataset. returns a dictionary in form of
    {"group title": list of download links corresponding to the group title}
    """
    base_url = url[:url.find("v") + 1]
    req = requests.get(url)
    soup = BeautifulSoup(req.content, features="html.parser")
    table_rows = soup.find_all("tr")
    links = {}
    for row in table_rows:
        table_data = row.find_all("td")
        for item in table_data:
            title = item.find("strong")
            if title and title not in links:
                links[title.text] = []
                continue
            link = item.find("a")
            if link:
                links[next(reversed(links.keys()))].append(base_url + link["href"])

    return links

class S3AWS:
    def __init__(self, access_key_id, secret_access_key):
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

    def ingest_from_usda(self, sources: list[str], bucket_name: str) -> None:
        source_list = [get_links(source) for source in sources]
        s3 = self.create_bucket(bucket_name=bucket_name) 

        for urls_dict in source_list: 
            for key, values in urls_dict.items():
                key = to_lowercase(key)        
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

def auth_credentials():
    load_dotenv()

class Ingestor():
    kaggle_sources = ["kaggle datasets download -d amanarora/obesity-among-adults-by-country-19752016"]
                    # "kaggle datasets download -d annedunn/obesity-and-gdp-rates-from-50-states-in-20142017",
                    # "kaggle datasets download -d spittman1248/cdc-data-nutrition-physical-activity-obesity"]    
    usda_sources = [
        "https://www.ers.usda.gov/data-products/commodity-consumption-by-population-characteristics/"]
    #     "https://www.ers.usda.gov/data-products/food-availability-per-capita-data-system/",
    #     "https://www.ers.usda.gov/data-products/food-consumption-and-nutrient-intakes/",
    #     "https://www.ers.usda.gov/data-products/eating-and-health-module-atus/",
    #     "https://www.ers.usda.gov/data-products/food-price-outlook/",
    #     "https://www.ers.usda.gov/data-products/food-expenditure-series/"
    # ]

    def __init__(self, source: str, s3: S3AWS):
        self.source = source
        self.s3 = s3 

    def ingest_data(self):
        if self.source == "kaggle":
            s3.ingest_from_kaggle(self.kaggle_sources, "s3-bucket-raw-kaggle")
        elif self.source == "usda":
            s3.ingest_from_usda(self.usda_sources, "s3-bucket-raw-usda")
        
if __name__ == "__main__":
    auth_credentials() 
    
    s3 = S3AWS(os.getenv("ACCESS_KEY_ID"),os.getenv("SECRET_ACCESS_KEY"))
    ingestor_kaggle = Ingestor("kaggle", s3)
    ingestor_kaggle.ingest_data()















