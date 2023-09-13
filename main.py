from fastapi import FastAPI
from domain.auth import auth_router
from domain.user import user_router
from domain.game import game_router
from domain.major import major_router
import models
from database import engine
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="iip5eJeoBlpcWFBwv49urb10j6bITMDWmNhxfRIe")

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

app.include_router(auth_router.router)
app.include_router(user_router.router)
# app.include_router(game_router.router)
# app.include_router(major_router.router)
