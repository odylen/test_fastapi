from fastapi import FastAPI, status, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn
from fastapi_pagination import add_pagination

from app.api.auth.api import router as auth_router
from app.api.bakery.api import router as bakery_router
from app.api.bonus_card.api import router as bonus_router
from app.api.campaign.api import router as campaign_router
from app.api.categories.api import router as category_router
from app.api.product.api import router as product_router
from app.api.promocode.api import router as promocode_router
from app.api.user.api import router as user_router
from database.db import Base, engine

load_dotenv()

Base.metadata.create_all(bind=engine)

origins = []

app = FastAPI()
api_router = APIRouter(prefix="/api")

api_router.include_router(auth_router)
api_router.include_router(bonus_router)
api_router.include_router(campaign_router)
api_router.include_router(user_router)
api_router.include_router(category_router)
api_router.include_router(product_router)
api_router.include_router(bakery_router)
api_router.include_router(promocode_router)
app.include_router(api_router)

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
    return {"message": "Hello World!"}


if __name__ == "__main__":
    uvicorn.run(app)
