import asyncio

from Database.Sqlbase import fetch_news_via_id
from StoreNews.genralscraper import get_data
from config import llm3

readtimedata = ""
def details(news_id):
    query = fetch_news_via_id(news_id)
    data = get_data(query[0])
    prompt_template = f"""
You are a News Assistant. Your task is to generate a fully detailed news article from raw news data.

Instructions:
- Use the provided raw text content to write a complete news article in a formal, professional tone.
- The article must be at least 1000 words long and read like a real journalistic piece.
- Do not summarize. Expand all relevant points into a proper narrative structure.
- Do not include irrelevant or fabricated information (e.g., fake quotes, made-up people like Pope Leo XIV).
- Avoid repetition and contradiction.
- Your output must be a **valid Python string object**, enclosed in triple quotes.

Raw News:
\"\"\"{data}\"
\"\"\"
"""



    return prompt_template

async def stream_details(news_id):
    llm_input = details(news_id)
    async for chunk in llm3.astream(llm_input):
        yield chunk.content

async def stream():
    global readtimedata
    async for data in stream_details(1):
        readtimedata = readtimedata + data
        print(data)

def read_time_eval(data):
    words = data.split()
    readtime = len(words)//200
    return max(readtime,1)


if __name__ == '__main__':
    asyncio.run(stream())
    print(read_time_eval(readtimedata))