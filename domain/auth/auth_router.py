# # auth/routes.py

# from fastapi import APIRouter, Depends
# from .models import User, UserCreate, UserRead, UserUpdate
# from .libs import auth_backend, current_active_user, fastapi_users

# router = APIRouter()

# get_auth_router = fastapi_users.get_auth_router(auth_backend)
# get_register_router = fastapi_users.get_register_router(UserRead, UserCreate)
# get_reset_password_router = fastapi_users.get_reset_password_router()
# get_verify_router = fastapi_users.get_verify_router(UserRead)
# get_users_router = fastapi_users.get_users_router(UserRead, UserUpdate)

# routers = [
#     (router, dict(prefix="/auth", tags=["auth"])),
#     (get_auth_router, dict(prefix="/auth/jwt", tags=["auth"])),
#     (get_register_router, dict(prefix="/auth", tags=["auth"])),
#     (get_reset_password_router, dict(prefix="/auth", tags=["auth"])),
#     (get_verify_router, dict(prefix="/auth", tags=["auth"])),
#     (get_users_router, dict(prefix="/users", tags=["users"])),
# ]

# @router.get("/authenticated-route")
# async def authenticated_route(user: User = Depends(current_active_user)):
#     return {"message": f"Hello {user.email}!"}










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
    # 클라이언트를 사용하여 토큰을 검증합니다.


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
    # 로그인한 유저가 있다면
    # user = None
    # try:
    #     user = await auth_google(request.session.get('user')) # client side is frontend(React). so we have to validate user by other method.
    # except Exception:
    #     pass


    # token_val = token_validation(request)
    # if token_val['validation']:
    #     pass
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
        # 성결대 이메일만 로그인할 수 있도록
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

        #HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized email domain.")
        # 로그인한 유저 정보를 세션에 할당
        # request.session['user'] = token['id_token'] # have to return JSON to Client side(React)

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
                "soccer": None,
                "basketball": None,
                "handball": None,
                "kickbaseball": None,
                "football": None,
                "dodgeball": None
            }

            db.add(new_user)
            db.commit()
        # else:
        #     existing_user.session = encoded_jwt
        #     db.add(existing_user)
        #     db.commit()
    return RedirectResponse(url=f'{redirect_url}?token={encoded_jwt}')

# @router.post('/logout') # no use
# async def logout(token: str , db: Session = Depends(get_db)): # have to send session data to backend (from front(React)) # request: Request
#     # 세션에서 유저 정보 삭제
#     # request.session.pop('user', None)
#     # user_token = request.session.get('token')
#     user_info = await decode_jwt(token)
#     user = await user_crud.get_user(db, user_info['email'])
#     user.session = '' # erase user.session
#     db.add(user)
#     db.commit()

#     return {
#         'validation': True, 
#         'message': 'logged out'}

