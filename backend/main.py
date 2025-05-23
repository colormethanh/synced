from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# To Run this app, type this in the terminal:
# uvicorn main:app --reload --port 8000

app = FastAPI()



# Allow React frontend to access FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/hello")
def read_root():
    return {"message": "Hello from FastAPI!"}


