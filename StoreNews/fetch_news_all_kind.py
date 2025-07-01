from StoreNews.hindustandscaper import scrape_ht_world_news_page
from StoreNews.genralscraper import smart_scrape
import threading

world_url = "https://www.hindustantimes.com/world-news/page-"
sports_url = "https://www.hindustantimes.com/sports/page-"
india_url = "https://www.hindustantimes.com/india-news/page-"
education_url = "https://www.hindustantimes.com/education/page-"
entertainment_url = "https://www.hindustantimes.com/entertainment/page-"
trending_url = "https://www.hindustantimes.com/trending/page-"

# Store links for each category
world = []
sports = []
india = []
education = []
entertainment = []
trending = []

lock = threading.Lock()

def fetch_news_link():
    def store_news_list(url,lis):
        out = list(set(scrape_ht_world_news_page(url)))
        lis.extend(out)
    threads = [threading.Thread(target=store_news_list,args=(world_url,world))
               ,threading.Thread(target=store_news_list,args=(sports_url,sports)),
               threading.Thread(target=store_news_list,args=(india_url,india))
               ,threading.Thread(target=store_news_list,args=(education_url,education))
               ,threading.Thread(target=store_news_list,args=(entertainment_url,entertainment)),
               threading.Thread(target=store_news_list,args=(trending_url,trending))]

    for t in threads:
        t.start()

    for t in threads:
        t.join()


    return world,sports,india,education,entertainment,trending
z = 0
def fetch_raw_data():
    world_news = []
    sports_news = []
    india_news = []
    education_news = []
    entertainment_news = []
    trending_news = []

    fetch_news_link()

    def store_news_data(urls,news_lis,type):
        global z
        for url in urls:
            out =  smart_scrape(url,type)
            news_lis.append(out)


    threads2 = [threading.Thread(target=store_news_data,args=(world,world_news,"World"))
               ,threading.Thread(target=store_news_data,args=(sports,sports_news,"Sports")),
               threading.Thread(target=store_news_data,args=(india,india_news,"India"))
               ,threading.Thread(target=store_news_data,args=(education,education_news,"Education"))
               ,threading.Thread(target=store_news_data,args=(entertainment,entertainment_news,"Entertainment")),
               threading.Thread(target=store_news_data,args=(trending,trending_news,"Trending"))]

    for t in threads2:
        t.start()

    for t in threads2:
        t.join()
    return world_news,sports_news,india_news,education_news,entertainment_news,trending_news

if __name__ == '__main__':
    out = fetch_raw_data()
    print(len(out))
    print(out)
    for i in out:
        for n,j in enumerate(i):
            print(n,j)
        print("_"*100)