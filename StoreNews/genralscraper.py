import requests
from bs4 import BeautifulSoup
from StoreNews.yahoosearchengine import yahoo_search
from langchain.agents import tool
import re
import threading
import random
data = []
lock = threading.Lock()
HEADERS_LIST = [
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Referer": "https://www.google.com/",
        "DNT": "1",
        "Cache-Control": "no-cache"
    },
    {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3_1) "
                      "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                      "Version/16.4 Safari/605.1.15",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.8",
        "Connection": "keep-alive",
        "Referer": "https://www.bing.com/",
        "Upgrade-Insecure-Requests": "1"
    },
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:112.0) Gecko/20100101 Firefox/112.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en;q=0.5",
        "Connection": "keep-alive",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1"
    },
    {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) "
                      "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                      "Version/16.4 Mobile/15E148 Safari/604.1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
        "Connection": "keep-alive"
    },
    {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/113.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "DNT": "1"
    },
    {
        "User-Agent": "Mozilla/5.0 (Linux; Android 12; SM-G991B) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Mobile Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-GB,en;q=0.5",
        "Referer": "https://www.google.com/",
        "Connection": "keep-alive"
    },
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:102.0) Gecko/20100101 Firefox/102.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5",
        "Upgrade-Insecure-Requests": "1",
        "Connection": "keep-alive"
    },
    {
        "User-Agent": "Mozilla/5.0 (iPad; CPU OS 15_7 like Mac OS X) "
                      "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                      "Version/15.0 Mobile/15E148 Safari/604.1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Connection": "keep-alive",
        "Referer": "https://www.google.com/"
    },
    {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5",
        "DNT": "1",
        "Connection": "keep-alive"
    },
    {
        "User-Agent": "Mozilla/5.0 (Linux; Android 11; Pixel 4 XL) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/117.0.0.0 Mobile Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Referer": "https://www.bing.com/"
    }
]


def extract_image_url(soup, domain):
    # Hindustan Times
    if "hindustantimes.com" in domain:
        container = soup.find('div', class_='storyParagraphFigure')
        if container:
            image = container.find('img')
            if image:
                image_url = image.get('src')
                if image_url and "default" not in image_url.lower():
                    return image_url
        return "No_image"

    # Indian Express
    elif "indianexpress.com" in domain:
        container = (
            soup.find('span',class_ = 'custom-caption')
        )
        if container:
            image = container.find('img')
            if image:
                image_url = image.get('src') or image.get('data-src')
                if image_url and "default" not in image_url.lower():
                    return image_url
        return "No_image"

    # Other unsupported domains
    return "No_image"

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

def smart_scrape(url, section=None):
        print(f"⚠⚠ Running for Url[{url}] || Type : {section} ⚠⚠")
        info = dict()
        temp_lis_h = []
        temp_lis_p = []
        headers = random.choice(HEADERS_LIST)

        res = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, "html.parser")

        # Try to get titles, headlines, paragraphs
        headlines = soup.find_all(["h1", "h2", "h3"], limit=20)
        paragraphs = soup.find_all("p")
        info["image_url"] = extract_image_url(soup, url)

        for h in headlines:
            temp_lis_h.append("📰 " + h.get_text(strip=True))
        for p in paragraphs:
            temp_lis_p.append("📄 " + p.get_text(strip=True))
        info["headlines"] = temp_lis_h
        info["Paragraphs"] = list(set(temp_lis_p))
        info["source"] = url
        if section != None:
            info["section"] = section
        return info

@tool
def get_data(querry:str):
    """
    This function Provides Data Using web search and scraping.
    :param querry: String to be searched on web.
    :return: list of dictionaries
    """
    print("Tool used for query : ",querry)
    global data
    data = []
    threads = []

    def run_scrape(url):
        out = smart_scrape(url)
        with lock:
            data.append(out)

    urls = yahoo_search(querry)
    for url in urls:
        try:
            t = threading.Thread(target=run_scrape,args=(url,))
            threads.append(t)
        except Exception as e:
            print("Error from the get_data tool:- ",e)

    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return data

if __name__ == '__main__':
    # print(get_data("india and pakistan war"))
    out= smart_scrape("https://indianexpress.com/article/cities/chandigarh/rs-49000-crore-ponzi-scheme-pacl-gurnam-singh-arrest-10119769/?ref=hometop_hp")
    print(out)
    print(len(out))