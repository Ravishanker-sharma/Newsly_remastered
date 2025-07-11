from StoreNews.hindustandscaper import scrape_ht_world_news_page
from StoreNews.genralscraper import smart_scrape
from StoreNews.Indianexpressscraper import fetch_india_news_links
import threading

world_url = ["https://www.hindustantimes.com/world-news","https://indianexpress.com/section/world/page/1/"]
sports_url = ["https://www.hindustantimes.com/sports","https://indianexpress.com/section/sports/page/1/"]
india_url = ["https://www.hindustantimes.com/india-news","https://indianexpress.com/section/india/page/1/"]
education_url = ["https://www.hindustantimes.com/education","https://indianexpress.com/section/education/page/1/"]
entertainment_url = ["https://www.hindustantimes.com/entertainment","https://indianexpress.com/section/entertainment/page/1/"]
trending_url = ["https://www.hindustantimes.com/trending","https://indianexpress.com/section/trending/page/1/"]

# Store links for each category
world = []
sports = []
india = []
education = []
entertainment = []
trending = []

lock = threading.Lock()
lock2 = threading.Lock()

def fetch_news_link():
    def hinduT_news_list(url,lis):
        out = list(set(scrape_ht_world_news_page(url)))
        with lock2:
            lis.extend(out)

    def indianex_news_list(url,lis):
        out = fetch_india_news_links(url)
        with lock2:
            lis.extend(out)
    threads = [threading.Thread(target=hinduT_news_list,args=(world_url[0],world))
               ,threading.Thread(target=hinduT_news_list,args=(sports_url[0],sports)),
               threading.Thread(target=hinduT_news_list,args=(india_url[0],india))
               ,threading.Thread(target=hinduT_news_list,args=(education_url[0],education))
               ,threading.Thread(target=hinduT_news_list,args=(entertainment_url[0],entertainment)),
               threading.Thread(target=hinduT_news_list,args=(trending_url[0],trending)),
               threading.Thread(target=indianex_news_list,args=(world_url[1],world))
               ,threading.Thread(target=indianex_news_list,args=(sports_url[1],sports)),
               threading.Thread(target=indianex_news_list,args=(india_url[1],india))
               ,threading.Thread(target=indianex_news_list,args=(education_url[1],education))
               ,threading.Thread(target=indianex_news_list,args=(entertainment_url[1],entertainment)),
               threading.Thread(target=indianex_news_list,args=(trending_url[1],trending))]

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
    # out = fetch_raw_data()
    # print(len(out))
    # print(out)
    # for i in out:
    #     for n,j in enumerate(i):
    #         print(n,j)
    #     print("_"*100)
    print(fetch_news_link())