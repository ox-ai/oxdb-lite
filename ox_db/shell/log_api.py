from ox_db.shell.log import run,db

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS for the frontend
origins = [
    "http://localhost:5173",  # React frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
def get():
    res = db.info()
    return res

@app.post("/run")
def push(script:str):
    try:
        result = run(script)
   
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return result





