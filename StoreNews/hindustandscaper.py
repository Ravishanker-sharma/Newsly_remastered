import requests
from bs4 import BeautifulSoup


def scrape_ht_world_news_page(url,page_num=1):
    url = f"{url}{page_num}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # HT seems to use <h3 class="hdg3"> for headlines inside <a>
    articles = soup.select("div.cartHolder a")

    results = []
    for a in articles:
        # headline = a.get_text(strip=True)
        link = a['href']
        if link.startswith('/'):
            link = "https://www.hindustantimes.com" + link
        results.append(link)

    return results


if __name__ == "__main__":
    scraped = scrape_ht_world_news_page()
    print(scraped)
