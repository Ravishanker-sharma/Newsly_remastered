from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"] for specific frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/api/news")
def read_root(section:str):
    out =[
  {
    "id": "news_493",
    "headline": "Central Panel Returns Andhra Pradesh's Polavaram Project Proposal",
    "bulletPoints": [
      "An expert committee has returned Andhra Pradesh's proposal for the Polavaram-Banakacharla Link Project",
      "The committee suggested that Andhra Pradesh consult with the Central Water Commission (CWC) regarding interstate issues before submitting the proposal",
      "Telangana has opposed the project, claiming it would deprive the state of its rightful share in the Godavari waters",
      "The project aims to divert surplus Godavari river water to the Pennar basin through the Krishna river",
      "Telangana has proposed an alternative plan to divert Godavari waters to the Pennar basin via Krishna."
    ],
    "imageUrl": "https://www.hindustantimes.com/ht-img/img/2025/07/01/550x309/The-Telangana-government-argued-that-the-project-w_1751398120397.jpeg",
    "sourceIconUrl": "https://www.hindustantimes.com/india-news/central-panel-returns-andhra-s-polavaram-project-proposal-101751397352597.html",
    "typeIconUrl": "https://www.hindustantimes.com/ht-img/img/2025/07/01/550x309/The-Telangana-government-argued-that-the-project-w_1751398120397.jpeg",
    "section": "india",
    "source": "Hindustan Times",
    "type": "Breaking News"
  },
  {
    "id": "news_491",
    "headline": "Telangana Factory Blast Toll Rises to 37, FIR Lodged",
    "bulletPoints": [
      "The death toll from the explosion at a pharmaceutical plant in the Sangareddy district of Telangana has risen to 37",
      "Rescue operations are ongoing to find at least 20 more people",
      "Chief Minister A Revanth Reddy has sought a detailed report on the incident and the police have registered an FIR against the management",
      "The government will provide compensation to the families of the deceased and medical care for the injured",
      "A special forensic team is assisting with post-mortem examinations and DNA sample collection."
    ],
    "imageUrl": "https://www.hindustantimes.com/ht-img/img/2025/07/01/550x309/Telangana-Chief-Minister-A-Revanth-Reddy-with-othe_1751397822469.jpg",
    "sourceIconUrl": "https://www.hindustantimes.com/india-news/telangana-blast-toll-rises-to-37-fir-lodged-101751397828839.html",
    "typeIconUrl": "https://www.hindustantimes.com/ht-img/img/2025/07/01/550x309/Telangana-Chief-Minister-A-Revanth-Reddy-with-othe_1751397822469.jpg",
    "section": "world",
    "source": "Hindustan Times",
    "type": "Breaking News"
  },
  {
    "id": "news_492",
    "headline": "India-US Trade Talks Enter Final Stage with All Possibilities on the Table",
    "bulletPoints": [
      "India and the US are in the final stage of trade talks, exploring all possibilities for an agreement",
      "Negotiations are focused on an interim deal with the potential for both countries to drop sensitive items",
      "The current talks aim to achieve tangible outcomes before July 9",
      "Failure to reach a deal could result in a 26% tariff on imports from India to the US",
      "Both countries are also discussing a comprehensive bilateral trade agreement (BTA)."
    ],
    "imageUrl": "https://www.hindustantimes.com/ht-img/img/2025/07/02/550x309/Trade-experts-said-an-interim-trade-deal-between-I_1751418045953_1751418058924.jpg",
    "sourceIconUrl": "https://www.hindustantimes.com/india-news/as-india-us-trade-talks-enter-final-stage-all-possibilities-still-on-table-101751417190899.html",
    "typeIconUrl": "https://www.hindustantimes.com/ht-img/img/2025/07/02/550x309/Trade-experts-said-an-interim-trade-deal-between-I_1751418045953_1751418058924.jpg",
    "section": "india",
    "source": "Hindustan Times",
    "type": "Breaking News"
  }
]

    return JSONResponse(content=out)


class ChatResponse(BaseModel):
  message: str
  conversation_id: str
  timestamp: str
class ChatRequest(BaseModel):
  user_id: str
  message: str
  news_id: Optional[str] = None
  conversation_id: Optional[str] = None
@app.post("/api/chat")
def chat(message:ChatRequest):
  print(message)
  return ChatResponse(message="hello",conversation_id="123",timestamp="123")