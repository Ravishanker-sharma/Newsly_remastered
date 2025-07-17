from StoreNews.genralscraper import get_data
from config import llm3
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel

class AgentOutput(BaseModel):
    headline: str
    fullContent: list
    source: str
    type: str
    publishedAt: str  # You can use datetime if you want
    readTime: int


def search(query):
    n = 0
    data = get_data(query)
    prompt_template = """
You are a News assistant. Convert the raw news data into a structured JSON object.

Rules:
- Do not add opinions.
- fullContent must be 10 to 15 bullet points , containing every crucial information.
- Output must be a **valid JSON** object only.
- In source , only use namest of the news source upto 3 names. 
Raw News:
{raw_news}

Respond in this format (don’t explain anything):

```json
{{
  "headline": "Your generated headline",
  "fullContent": ["Bullet Point 1", "Bullet Point 2", "Bullet Point 3", "Bullet Point 4", "Bullet Point N"],
  "source": "News Source",
  "type": "Breaking News",
  "publishedAt": "2024-07-08T10:00:00Z",
  "readTime": 4
}}"""
    print(data)
    prompt = PromptTemplate(
        input_variables=["raw_news"],
        template=prompt_template
    )

    while n<3:
        try:
            parser = PydanticOutputParser(pydantic_object=AgentOutput)

            chain = LLMChain(llm=llm3, prompt=prompt, output_parser=parser)

            output = (chain.run({"raw_news": data})).dict()
            output["id"] = "123"
            if query[4] == None or query[4] == "No_image" or query[4] == "":
                output[
                    "imageUrl"] = r"https://res.cloudinary.com/dxysb8v1a/image/upload/fl_preserve_transparency/v1751529660/newslylogo_eyrc2v.jpg"
            else:
                output["imageUrl"] = query[4]
            return output
        except Exception as e:
            print(e)
            n += 1
            continue
