from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from newsly_chat_bot.chat_bot import chat as newsly_chat
from Database.Sqlbase import Format_news
from datetime import datetime,timezone


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"] for specific frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/news")
def read_root(section:str, page: int = 1, user_id: Optional[str] = None, limit: Optional[int] = 20):
    section = section.capitalize()
    print(section)
    out = Format_news(page,section,limit)
    print(page)
    print(user_id)
    return JSONResponse(content=out)


class ChatResponse(BaseModel):
  message: str
  conversation_id: str
  timestamp: str
class ChatRequest(BaseModel):
  user_id: str
  message: str
  news_id: Optional[int] = "123"
  conversation_id: Optional[str] = None
@app.post("/api/chat")
def chat(message:ChatRequest):
    output = newsly_chat(message.message,message.news_id)
    currenttime = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return ChatResponse(message=str(output),conversation_id='123',timestamp=currenttime)


class FeedbackRequest(BaseModel):
    user_id: str
    news_id: str
    feedback: str  # "like" or "dislike"

class FeedbackResponse(BaseModel):
    status: str

@app.post("/api/feedback",response_model=FeedbackResponse)
def feedback(feedback: FeedbackRequest):
    print("Received payload:", feedback)
    if feedback.feedback == "like":
        newsly_chat(f"Thanks for liking the news",feedback.news_id)
        return {"status":"success"}
    elif feedback.feedback == "dislike":
        newsly_chat(f"Thanks for disliking the news",feedback.news_id)
        return {"status":"success"}
    else:
        return {"status":"failure"}