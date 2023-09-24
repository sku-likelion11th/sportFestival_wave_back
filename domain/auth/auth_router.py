from urllib.parse import quote
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from domain.user import user_schema, user_crud
from models import User
from authlib.integrations.starlette_client import OAuth, OAuthError
from starlette.requests import Request
from starlette.config import Config
from starlette.responses import HTMLResponse, RedirectResponse
import json
from fastapi.security import OAuth2PasswordBearer#, OAuthError
from fastapi.security.oauth2 import OAuth2PasswordBearer
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from google.oauth2 import id_token
import google
from dotenv import load_dotenv
import os
load_dotenv()

router = APIRouter()

oauth = OAuth(Config('.env'))
CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

oauth2_schema = OAuth2PasswordBearer(tokenUrl='/token')

@router.get('/google')
async def auth_google(token:str): # not router but function?
    try:
        idinfo = id_token.verify_oauth2_token(token, google.auth.transport.requests.Request(), os.getenv("GOOGLE_CLIENT_ID"))
        return idinfo
    except ValueError:
        return None


async def decode_jwt(token: str):
    payload = jwt.decode(token, os.environ["JWT_KEY"], 'HS256')
    return payload

@router.get('/validation')
async def token_validation(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)): # have to use every each function
    if token:
        try:
            payload = await decode_jwt(token)
            email = payload['email']
            user = await user_crud.get_user(db, email)
            if user:
                if datetime.now() <= datetime.strptime(payload["expire"], "%Y-%m-%d %H:%M:%S"):
                    # data = json.dumps(user)
                    return {
                            'validation': True,
                            'message': payload
                            }
                else:
                    #return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token has expired")
                    return {
                            'validation': False,
                            'message': 'expired'
                            }
            else:
                #return HTTPException(status_code=status.HTTP_404_UNAUTHORIZED, detail="no user found")
                return {
                        'validation': False, 
                        'message': 'no data'
                        }
        except:
            #return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token error")
            return {
                    'validation': False, 
                    'message': 'token error'
                    }
    else:
        #return HTTPException(status_code=status.HTTP_404_UNAUTHORIZED, detail="not logged in")
        return {
                'validation': False, 
                'message': 'not logged in'
                }


@router.get('/')
async def homepage(request: Request, db: Session = Depends(get_db)):
    return token_validation(request)




@router.get('/login')
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri, prompt='select_account')


@router.get('/auth')
async def auth(request: Request, db: Session = Depends(get_db)):
    redirect_url = 'http://wave-renew.sku-sku.com:3000/login/callback'
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        error_json = {
            'validation': False,
            'message': 'authorization error'
        }
        error_json = json.dumps(error_json)
        return RedirectResponse(url=f'{redirect_url}?error={error_json}')
    
    user = token.get('userinfo')
    if user:
        try:
            if user['hd'] != "sungkyul.ac.kr":
                error_json = {
                    'validation': False,
                    'message': 'Unauthorized'
                }
                error_json = json.dumps(error_json)
                return RedirectResponse(url=f'{redirect_url}?error={error_json}')
        except:
            error_json = {
                    'validation': False,
                    'message': 'Unauthorized email domain.'
                }
            error_json = json.dumps(error_json)
            return RedirectResponse(url=f'{redirect_url}?error={error_json}')

        expire_time_raw = datetime.utcnow() + timedelta(hours=10) # korean time + 1hour
        expire_time = expire_time_raw.strftime("%Y-%m-%d %H:%M:%S")
        _user = {
                'email': user['email'],
                'expire': expire_time
            }
        
        encoded_jwt = jwt.encode(_user, os.environ["JWT_KEY"], 'HS256')

        existing_user = await user_crud.get_user(db, user['email'])
        
        if not existing_user:
            new_user = User(email=user['email'], name=user['name'])#, session=encoded_jwt)
            new_user.games = { # insert games(JSON) like this.
                "축구": None,
                "농구": None,
                "손족구": None,
                "발야구": None,
                "족구": None,
                "피구": None
            }

            db.add(new_user)
            db.commit()

    return RedirectResponse(url=f'{redirect_url}?token={encoded_jwt}')
