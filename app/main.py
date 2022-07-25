from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn
from fastapi_pagination import add_pagination

load_dotenv()

from database.db import Base, engine
from routers import auth, bonus_card, campaign, user

Base.metadata.create_all(bind=engine)

origins = []

app = FastAPI()

app.include_router(auth.router)
app.include_router(bonus_card.router)
app.include_router(user.router)
app.include_router(campaign.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
add_pagination(app)
@app.get("/", status_code=status.HTTP_200_OK, tags=["API Check"])
def check():
    return {
        "message": "Hello World!"
    }

if __name__ == '__main__':
    uvicorn.run(app)