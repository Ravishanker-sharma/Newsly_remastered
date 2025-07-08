from Database.Sqlbase import fetch_news_via_id
from StoreNews.genralscraper import get_data
from config import llm
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import List,Dict

class AgentOutput(BaseModel):
    headline: str
    fullContent: str
    source: str
    type: str
    publishedAt: str  # You can use datetime if you want
    readTime: int


def details(news_id):
    query = fetch_news_via_id(news_id)
    data = get_data(query[4])
    prompt_template = """
    You are a News assistant. Convert the raw news data into a structured JSON object.

    Rules:
    - Do not add opinions.
    - fullContent must be very detailed (450+ words).
    - Output must be a **valid JSON** object only.


    Respond in this format (don’t explain anything):

    ```json
    {{
      "headline": "Your generated headline",
      "fullContent": "Very detailed article here...",
      "source": "News Source",
      "type": "Breaking News",
      "publishedAt": "2024-07-08T10:00:00Z",
      "readTime": 4
    }}```
    """
    prompt = PromptTemplate.from_template(prompt_template)

    parser = PydanticOutputParser(pydantic_object=AgentOutput)

    chain = LLMChain(llm=llm, prompt=prompt, output_parser=parser)

    output = (chain.run(question=data)).dict()
    output["id"] = news_id
    if query[4] == None or query[4] == "No_image" or query[4] == "":
        output[
            "imageUrl"] = r"https://res.cloudinary.com/dxysb8v1a/image/upload/fl_preserve_transparency/v1751529660/newslylogo_eyrc2v.jpg"
    else:
        output["imageUrl"] = query[4]
    return output


