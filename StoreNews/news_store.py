from config import llm,extract_json_from_llm_output
from StoreNews.fetch_news_all_kind import fetch_raw_data
import threading
import time
from Database.Sqlbase import update_news_data

page = 1  # Will try to implement later
final_data = []
lock = threading.Lock()

# Distinguished Raw News Data
whole_data = fetch_raw_data()
world_news = whole_data[0]
sports_news = whole_data[1]
india_news = whole_data[2]
education_news = whole_data[3]
entertainment_news = whole_data[4]
trending_news = whole_data[5]
print(whole_data)
instruction = """
You will be provided with News data containing news in format of List[dictionary].
Each Dictionary item is a different news.
For every dictionary item , create a headline , create bullet points [4 to 5].
If a News item is repeated Skip that news. (create it only once).
You will get Image link ,section and Source link too , do not interrupt them.(If you can't find a 'image_url' key in the dict item just add it , and set value to 'No_image')
Data will contain Irrelevant stuff , filter that out.
If you do not have enough data to create 4 to 5 bullet points , skip that news.
Your bulleted Points should be unbiased.
Also add what type of news it is for example innovation , breaking news , terror , crime etc.
Also create some (4 to 5) FAQs based on  the News and add them as a value to the Key: faq.
Finally provide output in this format:
    List[Dictionary]
    Example Output:
        ```json
        [{'image_url': 'url', 'headline': 'headline', 'Paragraphs': ['point1','point2','point3','point4'],'section':'section', 'source': 'Source_url','type':'type','faq':['faq1','faq2','faq3']},{'image_url': 'url', 'headline': 'headline', 'Paragraphs': ['point1','point2','point3','point4'] ,'section':'section','source': 'Source_url'},'type':'type','faq':['faq1','faq2','faq3']
        ```

"""

def build_outputs(data):
    prompt = f"Instruction : {instruction}; Raw News Data : {data}"
    output = llm.invoke(prompt).content
    return extract_json_from_llm_output(output)


def runner():
    global page
    print("Runner Is Executed!")
    def get_output(lis):
        if lis:
            out = build_outputs(lis[:30])
            del lis[:30]
            with lock:
                final_data.extend(out)

        else:
            print("List is empty")

    threads = [threading.Thread(target=get_output,args=(world_news,))
               ,threading.Thread(target=get_output,args=(sports_news,)),
               threading.Thread(target=get_output,args=(india_news,))
               ,threading.Thread(target=get_output,args=(education_news,))
               ,threading.Thread(target=get_output,args=(entertainment_news,)),
               threading.Thread(target=get_output,args=(trending_news,))]

    for t in threads:
        t.start()
    for t in threads:
        t.join()


def main():
    global final_data
    runner()
    result = final_data
    print("Final Data:",result)
    with open(r'/Users/ravisharma/PycharmProjects/Newsly_remastered/Database/temp.txt', 'w', encoding='utf-8') as f:
        f.write(str(result))
    update_news_data()
    final_data = []
    if world_news or sports_news or india_news or education_news or entertainment_news or trending_news:
        print("~" * 25, "Length", "~" * 25)
        print(len(world_news))
        print(len(sports_news))
        print(len(india_news))
        print(len(education_news))
        print(len(entertainment_news))
        print(len(trending_news))
        print(len(final_data))
        print("Found Items in the List, Sleeping for 100 secs.")
        time.sleep(100)
        main()


if __name__ == '__main__':
    main()
    print(final_data)