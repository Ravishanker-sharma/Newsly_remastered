import requests
from bs4 import BeautifulSoup
from yahoosearchengine import yahoo_search
from langchain.agents import tool
import re

data = []

def contains_binary_or_corrupt(text: str) -> bool:
    # Detects replacement characters (�)
    if '�' in text:
        return True

    # Detects escape-like sequences such as \x1c, \u07be
    if re.search(r'(\\x[0-9a-fA-F]{2})|(\\u[0-9a-fA-F]{4})', text):
        return True

    # Detects actual non-printable ASCII characters (0x00 to 0x1F except common ones like \n, \t)
    if any(ord(c) < 32 and c not in '\n\t\r' for c in text):
        return True

    return False

def smart_scrape(url,type=None):
        print(f"⚠⚠ Running for Url[{url}] || Type : {type} ⚠⚠")
        info = dict()
        temp_lis_h = []
        temp_lis_p = []
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/123.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "DNT": "1",  # Do Not Track
            "Upgrade-Insecure-Requests": "1",
            "Referer": "https://www.google.com/",
            "Cache-Control": "no-cache",
        }

        res = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, "html.parser")

        # Try to get titles, headlines, paragraphs
        headlines = soup.find_all(["h1", "h2", "h3"], limit=20)
        paragraphs = soup.find_all("p")
        container = soup.find('div', class_='storyParagraphFigure')
        if container:
            image = container.find('img')
            if image:
                image_url = image['src']
                if "default" in str(image_url).lower():
                    info["image_url"] = "No_image"
                else:
                    info["image_url"] = image_url
            else :
                info["image_url"] = "No_image"

        for h in headlines:
            temp_lis_h.append("📰 " + h.get_text(strip=True))
        for p in paragraphs:
            temp_lis_p.append("📄 " + p.get_text(strip=True))
        info["headlines"] = temp_lis_h
        info["Paragraphs"] = list(set(temp_lis_p))
        info["source"] = url
        if type != None:
            info["type"] = type
        return info

@tool
def get_data(querry:str):
    """
    This function Provides Data Using web search and scraping.
    :param querry: String to be searched on web.
    :return: String of data
    """
    print("Tool used for query : ",querry)
    global data
    data = []
    urls = yahoo_search(querry)
    for url in urls:
        try:
            data.append(smart_scrape(url))
        except Exception as e:
            print("Error from the get_data tool:- ",e)
    return data

if __name__ == '__main__':
    print(get_data("india and pakistan war"))
    # out= smart_scrape("https://www.hindustantimes.com/cities/delhi-news/delhi-ndft-seeks-ugc-rule-change-recognition-for-ad-hoc-du-teachers-101750703296295.html")
    # print(out)
    # print(len(out))