from fastapi import FastAPI
# from database import engine
from domain.user import user_router
from domain.game import game_router
from domain.major import major_router
import models
from database import engine
from starlette.middleware.cors import CORSMiddleware
app = FastAPI()


origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


models.Base.metadata.create_all(bind=engine) # create all tables in models.py on MySQL


app.include_router(user_router.router)
app.include_router(game_router.router)
app.include_router(major_router.router)
