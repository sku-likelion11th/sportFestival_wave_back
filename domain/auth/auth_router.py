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



from google.oauth2 import id_token
import google
from dotenv import load_dotenv
import os
load_dotenv()

@router.get('/google')
async def auth_google(token:str):
    try:
        idinfo = id_token.verify_oauth2_token(token, google.auth.transport.requests.Request(), os.getenv("GOOGLE_CLIENT_ID"))
        return idinfo
    except ValueError:
        return None
    # 클라이언트를 사용하여 토큰을 검증합니다.






@router.get('/')
async def homepage(request: Request):
    # 로그인한 유저가 있다면
    user = None
    try:
        user = await auth_google(request.session.get('user'))
    except Exception:
        pass
    if user:
        # data = json.dumps(user)
        html = (
            f'<pre>{user}</pre>'
            '<a href="/logout">logout</a>'
        )
        return HTMLResponse(html)
    return HTMLResponse('<a href="/login">login</a>')

@router.get('/login')
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri, prompt='select_account')


@router.get('/auth')
async def auth(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')
    
    user = token.get('userinfo')
    if user:
        # 성결대 이메일만 로그인할 수 있도록
        if user['hd'] != "sungkyul.ac.kr":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized email domain.")
        # 로그인한 유저 정보를 세션에 할당
        request.session['user'] = token['id_token']
        existing_user = user_crud.get_user_by_email(db, email=user['email'])
        
        if not existing_user:
            new_user = User(email=user['email'], name=user['name'])
            new_user.games = {
                "soccor": None,
                "basketball": None
            }
            db.add(new_user)
            db.commit()

    return RedirectResponse(url='/')

@router.get('/logout')
async def logout(request: Request):
    # 세션에서 유저 정보 삭제
    request.session.pop('user', None)
    return RedirectResponse(url='/')
















