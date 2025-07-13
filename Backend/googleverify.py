from fastapi import HTTPException
from pydantic import BaseModel
from google.oauth2 import id_token
from google.auth.transport import requests as grequests


GOOGLE_CLIENT_ID = "46098886946-bc3j612rc9je4slsvuaqa72m03g9i7ke.apps.googleusercontent.com"

def google_auth(data):
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

        # 👉 This is now a trusted user. You can:
        # - Save them to your database
        # - Create a session or token
        # - Return success response

        return {
            "message": "Google login verified ✅",
            "user": {
                "google_id": google_id,
                "email": email,
                "name": name,
                "picture": picture,
                "age": data.age  # optional, came from frontend
            }
        }

    except ValueError as e:
        raise HTTPException(status_code=401, detail="Invalid Google token")

