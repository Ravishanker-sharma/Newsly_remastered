import requests
from bs4 import BeautifulSoup


def scrape_ht_world_news_page(url,page_num=1):
    # url = f"{url}{page_num}"
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "

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
    except Exception as e:
        print(f"Error: {e}")
        return []


if __name__ == "__main__":
    scraped = scrape_ht_world_news_page("https://www.hindustantimes.com/world-news")
    print(scraped)