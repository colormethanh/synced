from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import httpx
from dotenv import load_dotenv

# To Run this app, type this in the terminal:
# uvicorn main:app --reload --port 8000


load_dotenv()

app = FastAPI()


GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8000/auth/google/callback"


# Allow React frontend to access FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TokenRequest(BaseModel):
    code: str


@app.get("/api/hello")
def read_root():
    return {"message": "Hello from FastAPI!"}



@app.get("/auth/google")
async def google_auth_url():
    return {
        "auth_url": (
            f"https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={GOOGLE_CLIENT_ID}&"
            f"redirect_uri={REDIRECT_URI}&"
            f"response_type=code&"
            f"scope=https://www.googleapis.com/auth/calendar.readonly&"
            f"access_type=offline&"
            f"prompt=consent"
        )
    }


@app.get("/auth/google/callback")
async def google_callback(request: Request):
    code = request.query_params.get("code")
    async with httpx.AsyncClient() as client:
        token_resp = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uri": REDIRECT_URI,
                "grant_type": "authorization_code",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
    token_json = token_resp.json()
    access_token = token_json.get("access_token")
    return {"access_token": access_token}

@app.get("/calendar")
def get_calendar_events():
    print("Retrieving calendar")
    pass

