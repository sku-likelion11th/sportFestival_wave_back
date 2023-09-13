from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from domain.user import user_schema, user_crud
from domain.game import game_schema
from models import User
from authlib.integrations.starlette_client import OAuth, OAuthError
from starlette.requests import Request
from starlette.config import Config
from starlette.responses import HTMLResponse, RedirectResponse
import json

router = APIRouter(
    prefix="/user",
)

# # don't use
# @router.get("/list")
# def user_list(db: Session = Depends(get_db), response_model=list[user_schema.User]):
#     _user_list = user_crud.get_user_list(db)
#     return _user_list

# # don't use
# @router.get("/detail/{user_id}", response_model=user_schema.User)
# def user_detail(user_id: int, db: Session = Depends(get_db)):
#     user = user_crud.get_user_by_id(db, user_id=user_id)
#     if user is None:
#         return HTMLResponse('no_user_detail')#RedirectResponse(url='/')
#     return user


@router.post('/info')
async def user_change(request: Request, user_data: user_schema.User, db: Session = Depends(get_db)):
    user = request.session.get('user')
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="로그인안함")
    userdb = db.query(User).filter_by(email=user["email"]).first()
    userdb.student_num = user_data.student_num
    userdb.phone_num = user_data.phone_num

    db.commit()
    return userdb
    
    
@router.get('/info')
async def user_info(request: Request, db: Session = Depends(get_db)):#, response_model=list[user_schema.User]):
    user = request.session.get('user')
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="로그인안함")
    userdb = db.query(User).filter_by(email=user["email"]).first()

    if userdb:
        return userdb.__dict__ # 모든 column 출력
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없음")
    

@router.get('/game')
async def user_game(request: Request, db:Session = Depends(get_db)):
    user = request.session.get('user')
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="로그인안함")
    userdb = db.query(User).filter_by(email=user["email"]).first()
    
    if userdb:
        return userdb.games
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없음")
    

# @router.post('/game')
# async def user_game(request: Request, game_data=game_schema.Game ,db:Session = Depends(get_db)):
#     user = request.session.get('user')
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="로그인안함")
#     userdb = db.query(User).filter_by(email=user["email"]).first()
#     if userdb:
#         games = userdb.games
#         if games:
#             # update game JSON object
#             pass
#         else:
#             # create a new game JSON object
#             pass
    
#         return games
#     else:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없음")