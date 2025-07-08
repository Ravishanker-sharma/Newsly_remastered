from fastapi import FastAPI,UploadFile,File,Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from config import convert_audio_to_text
import shutil
from newsly_chat_bot.chat_bot import chat as newsly_chat
from Database.Sqlbase import Format_news,login,fetch_news_via_id
from Database.vectordatabase import delete_existing,add_data
from datetime import datetime,timezone
from Backend.display_personalized_news import for_you_section

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
    if section == "For-you":
        return for_you_section(page, user_id, limit)
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
    news_id: int
    feedback: str  # "like" or "dislike"

class FeedbackResponse(BaseModel):
    status: str

@app.post("/api/feedback",response_model=FeedbackResponse)
def feedback(feedback: FeedbackRequest):
    doc_id = f"{feedback.user_id}_{feedback.news_id}"
    metadata = dict(news_id=feedback.news_id,user_id=feedback.user_id,feedback=feedback.feedback,doc_id=doc_id)
    news_data = fetch_news_via_id(metadata["news_id"])[1]
    print(news_data)
    delete_existing(metadata)
    add_data(news_data,metadata)
    if feedback.feedback == "like":
        return {"status":"success"}
    elif feedback.feedback == "dislike":
        return {"status":"success"}
    else:
        return {"status":"failure"}


class User(BaseModel):
    fullName: str
    age: int
    email: str

@app.post("/api/login")
def log_user(user: User):
    print("Received payload:", user.email)
    data = dict()
    data["email"] = user.email
    data["name"] = user.fullName
    data["age"] = user.age
    result = login(data)
    print("login results:",result[3])
    return {
  "user_id": result[3]
    }



@app.post("/api/chat/voice")
def chat_voice(
        audio: UploadFile = File(...),
    user_id: str = Form(...),
    news_id: Optional[str] = Form(None),
    conversation_id: Optional[str] = Form(None)
):
    file_path = "voice_message.wav"

    # Save uploaded file (overwrite if exists)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)

    result = convert_audio_to_text(file_path)
    output = newsly_chat(result, news_id)
    currenttime = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
  "message": output,
  "conversation_id": conversation_id,
  "timestamp": currenttime
}

@app.get("/api/chat/faqs")
def chat_faqs(newsId:str):
    faq = fetch_news_via_id(newsId)[3]
    faqs = faq.split("||")
    faq_lis = []
    for i, que in enumerate(faqs):
        d = dict()
        d["id"]=str(i)
        d["question"] = que
        faq_lis.append(d)
    return JSONResponse(faq_lis)