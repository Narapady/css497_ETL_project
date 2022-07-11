
import requests
from bs4 import BeautifulSoup

def download_xls_file(url: str) -> None:
    req = requests.get(url)
    filename = req.url[url.rfind("/") + 1: url.rfind("?")]

    with open(filename, "wb") as f:
        for chunk in req.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

def get_links(url: str):
    base_url = url[:url.find("v") + 1]

    req = requests.get(url)
    soup = BeautifulSoup(req.content, features="html.parser")
    table_rows = soup.find_all("tr")
    
    links = {}
    for row in table_rows:
        td = row.find_all("td")
        for item in td:
            title = item.find("strong")
            if title is not None and title not in links:
                links[title.text] = []
                continue

            link = item.find("a")
            if link:
                links[next(reversed(links.keys()))].append(base_url + link["href"])

    return links


if __name__ == "__main__":
    url = "https://www.ers.usda.gov/data-products/food-expenditure-series/"
    links = get_links(url)
    for key, value in links.items():
        print("key: ", key)
        print("Value: ", value)
