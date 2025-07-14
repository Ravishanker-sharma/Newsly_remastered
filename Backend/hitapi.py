import asyncio

from fastapi import FastAPI,UploadFile,File,Form,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from config import convert_audio_to_text
import shutil
from newsly_chat_bot.chat_bot import chat as newsly_chat
from Database.Sqlbase import Format_news,fetch_news_via_id,signup,check_user
from Database.vectordatabase import delete_existing,add_data
from datetime import datetime,timezone
from Backend.display_personalized_news import for_you_section
from Backend.Getdetails import details
from Backend.googleverify import google_auth
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"  ],  # or ["http://localhost:3000"] for specific frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "Backend Is online!"}
@app.get("/api/news")
def read_root(section:str, page: int = 1, user_id: Optional[str] = None, limit: Optional[int] = 20):
    print(f"🌐 /api/news hit with: section={section}, page={page}, user_id={user_id}, limit={limit}")

    section = section.capitalize()
    if section == "For-you" or section == "for-you":
        return for_you_section(page, user_id, limit)
    print(section)
    out = Format_news(page,section,limit)
    print(page)
    print(user_id)
    return out


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
async def chat(message:ChatRequest):
    currenttime = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if message.user_id.startswith("guest"):
        return ChatResponse(message="Sign in with your Google account to continue.", conversation_id='123', timestamp=currenttime)
    output = newsly_chat(message.message,message.news_id)
    currenttime = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(message.user_id)
    return ChatResponse(message=str(output),conversation_id='123',timestamp=currenttime)


class FeedbackRequest(BaseModel):
    user_id: str
    news_id: int
    feedback: str  # "like" or "dislike"

class FeedbackResponse(BaseModel):
    status: str

@app.post("/api/feedback",response_model=FeedbackResponse)
async def feedback(feedback: FeedbackRequest):
    if feedback.user_id.startswith("guest"):
        return {"status":"failure"}
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

class Log(BaseModel):
    email: str
    password: str
class User(BaseModel):
    fullName: str
    age: int
    email: str
    password: str

@app.post("/api/chat/voice")
async def chat_voice(
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
async def chat_faqs(newsId:str):
    if newsId == "null" or newsId == None or newsId == "" or newsId == " ":
        return JSONResponse([
    {'id': '0', 'question': 'What are the top news stories happening around the world today?'},
    {'id': '1', 'question': 'What is the current political situation in the country?'},
    {'id': '2', 'question': 'What are the major economic trends being reported in the news?'},
    {'id': '3', 'question': 'What are the biggest developments in science, health, or technology this week?'}
]
)
    faq = fetch_news_via_id(newsId)[3]
    faqs = faq.split("||")
    faq_lis = []
    for i, que in enumerate(faqs):
        d = dict()
        d["id"]=str(i)
        d["question"] = que
        faq_lis.append(d)
    print(faq_lis)
    return JSONResponse(faq_lis)

@app.get("/api/news/detailed")
async def news_detailed(news_id:str,user_id:str):
    if user_id.startswith("guest"):
        return JSONResponse({"message":"Sign in with your Google account to continue."})
    output = details(news_id)
    return output

@app.post("/api/register")
async def register(user: User):
    data = dict()
    data["email"] = user.email
    data["name"] = user.fullName
    data["age"] = user.age
    data["password"]=user.password
    if check_user(data) == 0:
        result = signup(data)
        print("signup results: Created user !")
        return {"user_id": result}
    else:
        print("signup results: Raised a error!")
        raise HTTPException(status_code=400, detail="Email already registered")


class GoogleAuth(BaseModel):
    credential: str
    fullName: str
    age: int
    email: str

@app.post("/api/auth/google")
async def auth_google(auth: GoogleAuth):
    google_data = google_auth(auth)
    return google_data