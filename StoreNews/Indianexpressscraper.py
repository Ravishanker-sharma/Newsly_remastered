import requests
from bs4 import BeautifulSoup
import random

# List of user-agent headers to rotate through
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:112.0) Gecko/20100101 Firefox/112.0",
    "Mozilla/5.0 (Linux; Android 12; SM-G996B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1"
]


# Base headers template
def get_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "DNT": "1",  # Do Not Track Request Header
        "Upgrade-Insecure-Requests": "1"
    }


def fetch_india_news_links(url):
    print(f"Fetching page {url}")

    try:
        response = requests.get(url, headers=get_headers(), timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Error {e}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    links = soup.find_all("a")

    article_urls = []
    for a in links:
        href = a.get("href")
        if href and "/article/" in href and href.startswith("https://indianexpress.com"):
            article_urls.append(href)

    return list(set(article_urls))  # remove duplicates


if __name__ == "__main__":
    links = fetch_india_news_links("https://indianexpress.com/section/india/page/1/")
    print(f"\n✅ Total Unique Articles Found: {len(links)}")
    for link in links:
        print(link)
