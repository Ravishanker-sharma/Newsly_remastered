from Database.vectordatabase import  query_base,probability_calculator
from Database.Sqlbase import get_news
import random

def for_you_section(page,user_id,limit=20):
    data = get_news(page_number=page,limit=limit)
    lisofprob = []
    for i in data:
        result = query_base(i[2], n=10, where={"user_id": user_id})
        lisofprob.append(probability_calculator(result))

    def select_top_25_mixed(news_data, prob_scores, threshold=0.6):
        # Pair each news with its probability
        paired = list(zip(prob_scores, news_data))

        # Separate high and low probability news
        high_prob = [item for item in paired if item[0] >= threshold]
        low_prob = [item for item in paired if item[0] < threshold]

        # Sort both by probability (optional for getting best of each group)
        high_prob.sort(key=lambda x: x[0], reverse=True)
        low_prob.sort(key=lambda x: x[0], reverse=True)

        # Select top 15 high and top 10 low
        selected_high = high_prob[:15]
        selected_low = low_prob[:10]

        # Combine and shuffle
        combined = selected_high + selected_low
        random.shuffle(combined)

        return combined

    res= select_top_25_mixed(data,lisofprob)

    def Format_news(data):
        probab = []
        news = []
        for a,b in data:
            probab.append(a)
            news.append(b)
        output = []
        for p,i in zip(probab,news):
            info = dict()
            info["id"] = i[0]
            info["headline"] = i[1]
            info["bulletPoints"] = i[2].split("..")
            if i[4] == None or i[4] == "No_image" or i[4] == "":
                info["imageUrl"] = r"https://res.cloudinary.com/dxysb8v1a/image/upload/fl_preserve_transparency/v1751529660/newslylogo_eyrc2v.jpg"
            else:
                info["imageUrl"] = i[4]
            info["sourceIconUrl"] = i[5]
            if "indianexpress.com" in i[5].lower():
                info["source"] = "Indian Express"
            elif "thehindu.com" in i[5].lower():
                info["source"] = "The Hindu"
            elif "thetimes.com" in i[5].lower():
                info["source"] = "The Times"
            elif "thehindubusinessline.com" in i[5].lower():
                info["source"] = "The Hindu Business Line"
            elif "thehindu.in" in i[5].lower():
                info["source"] = "The Hindu"
            elif "hindustantimes.com" in i[5].lower():
                info["source"] = "Hindustan Times"
            else:
                info["source"] = "Newsly"
            info["section"] = i[3].lower()
            info["type"] = i[6].capitalize()
            info["probability"] = round(p * 100, 2)
            output.append(info)
        return output

    return Format_news(res)