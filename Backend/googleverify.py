from fastapi import HTTPException
from Database.Sqlbase import signup,check_user
import os
from google.oauth2 import id_token
from google.auth.transport import requests as grequests
from dotenv import load_dotenv
load_dotenv()
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

def google_auth(data):
    try:
        userdata  =  check_user(data.email)
        if userdata:

            return{
                "message": "Google login verified ✅",
                "user": {
                    "user_id": userdata[3],
                    "email": userdata[4],
                    "name": userdata[1],
                    "picture": userdata[5],
                    "age": userdata[2]  # optional, came from frontend
                }
            }

    except Exception as e:
        print(e)
    try:

        # ✅ Verify token using Google lib
        idinfo = id_token.verify_oauth2_token(
            data.credential,
            grequests.Request(),
            GOOGLE_CLIENT_ID
        )

        # ❗ Re-check email is verified
        if not idinfo.get("email_verified"):
            raise HTTPException(status_code=403, detail="Email not verified")

        # ✅ Extract user data from token (this is trusted)
        google_id = idinfo["sub"]
        email = idinfo["email"]
        name = idinfo.get("name", "")
        picture = idinfo.get("picture", "")
        signup(google_id, email, name, picture, data.age)
        # 👉 This is now a trusted user. You can:
        # - Save them to your database
        # - Create a session or token
        # - Return success response

        return {
            "message": "Google login verified ✅",
            "user": {
                "user_id": google_id,
                "email": email,
                "name": name,
                "picture": picture,
                "age": data.age  # optional, came from frontend
            }
        }

    except ValueError as e:
        raise HTTPException(status_code=401, detail="Invalid Google token")

