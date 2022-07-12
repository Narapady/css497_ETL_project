import requests
import os
from bs4 import BeautifulSoup

def to_lowercase(word):
    result = word.split(" ")
    result = [item.lower() for item in result]
    return " ".join(result).replace(" ", "-")
    
def download_xls(urls_dict: dict[str, list[str]]) -> None:
    """
    Download xls files from  the urls_dicts into the current directory. The files are 
    downloaded into thier corresponding subdirectory. urls_dict key is the group title of the dataset
    and urls_dict value is a list that contians links to download dataset related to the group titile. 
    """ 
    for key, values in urls_dict.items():
        key = to_lowercase(key)        
        os.mkdir(key)
        os.chdir(key)
        for link in values:
            req = requests.get(link)
            filename = req.url[link.rfind("/") + 1: link.rfind("?")]
            with open(filename, "wb") as f:
                for chunk in req.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

        parent_path = os.path.dirname(os.getcwd())
        os.chdir(parent_path)

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

if __name__ == "__main__":
    urls = [
        "https://www.ers.usda.gov/data-products/commodity-consumption-by-population-characteristics/",
        "https://www.ers.usda.gov/data-products/food-availability-per-capita-data-system/",
        "https://www.ers.usda.gov/data-products/food-consumption-and-nutrient-intakes/",
        "https://www.ers.usda.gov/data-products/eating-and-health-module-atus/",
        "https://www.ers.usda.gov/data-products/food-price-outlook/",
        "https://www.ers.usda.gov/data-products/food-expenditure-series/"
    ]
    # for url in urls:
    #     links = get_links(url)
    #     download_xls(links)
    url = urls[-1]
    links = get_links(url)
    download_xls(links)


