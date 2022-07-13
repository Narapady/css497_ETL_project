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

def create_s3_bucket(bucket_name: str):
    client = boto3.client('s3', 
                       aws_access_key_id=os.getenv("ACCESS_KEY_ID"),
                       aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"))
    client.create_bucket(Bucket=bucket_name)
    return client


def upload_ers_to_s3(urls_dict: dict[str, list[str]], bucket_name: str) -> None:

    s3 = create_s3_bucket(bucket_name=bucket_name) 

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

def upload_kaggle_to_s3(bucket_name: str, api_commands: list[str]) -> None:

    s3 = create_s3_bucket(bucket_name) 
    for command in api_commands:
        os.system(command)
        filename = command.split("/")[1]
        with zipfile.ZipFile(filename + ".zip") as zip:
            zip.extractall()
            for file in os.listdir():
                if ".csv" in file:
                    s3.upload_file(file, bucket_name, "obesity/" + file)
            
        os.system("rm *.zip *.csv")


if __name__ == "__main__":
    urls = [
        "https://www.ers.usda.gov/data-products/commodity-consumption-by-population-characteristics/",
        "https://www.ers.usda.gov/data-products/food-availability-per-capita-data-system/",
        "https://www.ers.usda.gov/data-products/food-consumption-and-nutrient-intakes/",
        "https://www.ers.usda.gov/data-products/eating-and-health-module-atus/",
        "https://www.ers.usda.gov/data-products/food-price-outlook/",
        "https://www.ers.usda.gov/data-products/food-expenditure-series/"
    ]
    api_commands = ["kaggle datasets download -d amanarora/obesity-among-adults-by-country-19752016",
                    "kaggle datasets download -d annedunn/obesity-and-gdp-rates-from-50-states-in-20142017",
                    "kaggle datasets download -d spittman1248/cdc-data-nutrition-physical-activity-obesity"]
    load_dotenv()
    # for url in urls:
    #     links = get_links(url)
    #     download_xls(links)
    url = urls[-1]
    links = get_links(url)
    # download_xls(links)
    # upload_to_s3(links, "s3-bucket-raw-usda-ers")
    upload_kaggle_to_s3("s3-bucket-raw-kaggle", api_commands)    
