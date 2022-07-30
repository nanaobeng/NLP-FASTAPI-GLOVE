import sys, os

from services import *
from schemas import *

from typing import List
import fastapi as _fastapi
import fastapi.security as _security
import sqlalchemy.orm as _orm
from fastapi.middleware.cors import CORSMiddleware
import json 
import itertools

app = _fastapi.FastAPI()

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



@app.post("/auth/users")
async def create_user(
    user: UserCreate, db: _orm.Session = _fastapi.Depends(get_db)
):
    
    db_user = await get_user_by_email(user.email, db)
    if db_user:
        raise _fastapi.HTTPException(status_code=400, detail="Email already in use")

    user = await create_user(user, db)

    return await create_token(user)


@app.post("/auth/token")
async def generate_token(
    form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(),
    db: _orm.Session = _fastapi.Depends(get_db),
):
    user = await authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid Credentials")

    return await create_token(user)


@app.get("/auth/user", response_model=User)
async def get_user(user: User = _fastapi.Depends(get_current_user)):
    return user


@app.post("/words")
async def get_words(word: WordSearch = _fastapi.Depends(get_words)):
    return word

@app.get("/word")
def get_vector(word: str = _fastapi.Depends(get_vector)):
    return word

@app.post("/words/find/similar")
def similar_words(words: WordSearch = _fastapi.Depends(find_similar_words)):
    return words
 
@app.get("/")
def start():
    return {"welcome" : "Application is running"}
        
