import sys
import os
from pathlib import Path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from database import get_db
from api import router
import dotenv

dotenv.load_dotenv()
STATIC_PATH = os.getenv("STATIC_PATH")

app = FastAPI()

app.mount("/static", StaticFiles(directory=Path(STATIC_PATH)), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Your FastAPI app setup code here
app.include_router(router)


# Example of using the get_db function
@app.get("/")
async def root():
    db = next(get_db())
    # Use db to query your database
    return {"message": "Welcome to VMBook!"}

import logging
from requests import Request

@app.middleware("http") 
async def log_requests(request: Request, call_next): 
    logger = logging.getLogger(__name__)
    logger.info(f"Request: {request.method} {request.url}") 
    logger.info(f"Headers: {request.headers}") 
    body = await request.body() 
    logger.info(f"Body: {body}") 
    response = await call_next(request) 
    logger.info(f"Response status: {response.status_code}") 
    return response

if __name__ == "__main__":

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # or run with `uvicorn main:app --reload --host 0.0.0.0` in the terminal
    