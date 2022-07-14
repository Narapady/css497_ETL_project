import requests
from bs4 import BeautifulSoup


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
