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

@router.get('/')
async def homepage(request: Request):
    # 로그인한 유저가 있다면
    user = request.session.get('user')
    print(user)
    if user:
        data = json.dumps(user)
        html = (
            f'<pre>{data}</pre>'
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
        request.session['user'] = user
        existing_user = user_crud.get_user_by_email(db, email=user['email'])

        if not existing_user:
            new_user = User(email=user['email'], name=user['name'])
            db.add(new_user)
            db.commit()

    return RedirectResponse(url='/')

@router.get('/logout')
async def logout(request: Request):
    # 세션에서 유저 정보 삭제
    request.session.pop('user', None)
    return RedirectResponse(url='/')
