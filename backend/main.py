from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import os
import httpx
from dotenv import load_dotenv

# To Run this app, type this in the terminal:
# uvicorn main:app --reload --port 8000


load_dotenv()

app = FastAPI()


# Allow React frontend to access FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://192.168.2.133:3000"],  # frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware, 
    secret_key=os.getenv("SESSION_SECRET_KEY"),
    https_only=False      # ✅ allows cookies over HTTP (needed for localhost)), TODO: delete this later
)
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
print(GOOGLE_CLIENT_ID)
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8000/auth/google/callback"
print(GOOGLE_CLIENT_SECRET)



class TokenRequest(BaseModel):
    code: str


@app.get("/api/hello")
def read_root():
    return {"message": "Hello from FastAPI!"}

@app.get("/auth/status")
def auth_status(request: Request):
    print("Session contents:", request.session)
    token = request.session.get("access_token")
    return {"authenticated": bool(token)}

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
    refresh_token = token_json.get("refresh_token")

    # TODO: In the future we will def. be saving these to the db or alongside a userid
    print(f"Setting session data: {request.session}")
    request.session["access_token"] = access_token
    request.session["refresh_token"] = refresh_token
    print(f"Just set session data: {request.session}")

    return RedirectResponse(url="http://localhost:3000/sync")

@app.get("/calendar")
async def get_calendar_events(request: Request):
    print("Retrieving calendar")
    access_token = request.session.get("access_token")

    if not access_token:
        return JSONResponse(status_code=401, content={"error": "Not authenticated"})
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    params = {
        "maxResults": 10,
        "orderBy": "startTime",
        "singleEvents": True,
        "timeMin": "2024-06-01T00:00:00Z"  # optional: only fetch upcoming events
    }

    url = "https://www.googleapis.com/calendar/v3/calendars/primary/events"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)

    if response.status_code != 200:
        return JSONResponse(status_code=response.status_code, content=response.json())

    return response.json()
    



