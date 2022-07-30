import sys, os
import database as _database, models as _models
from schemas import *
import fastapi as _fastapi
import fastapi.security as _security
import jwt as _jwt
import datetime as _dt
import sqlalchemy.orm as _orm
import passlib.hash as _hash
import numpy as np
from scipy import spatial
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

oauth2schema = _security.OAuth2PasswordBearer(tokenUrl="/api/token")

JWT_SECRET = "KRGgwyVV4yF0aFvVeh6X"

embeddings_dict = {}
with open("./file/glove.6B.50d.txt", 'r', encoding="utf-8") as f:
    for line in f:
        values = line.split()
        key_word = values[0]
        vector = np.asarray(values[1:], "float32")
        if len(key_word) > 2:
            embeddings_dict[key_word] = vector


def create_db():
    return _database.Base.metadata.create_all(bind=_database.engine)


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_user_by_email(email: str, db: _orm.Session):
    return db.query(_models.User).filter(_models.User.email == email).first()


async def create_user(user: UserCreate, db: _orm.Session):
 


    user_obj = _models.User(
        email=user.email, hashed_password=_hash.bcrypt.hash(user.hashed_password)
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


async def authenticate_user(email: str, password: str, db: _orm.Session):
    user = await get_user_by_email(db=db, email=email)

    if not user:
        return False

    if not user.verify_password(password):
        return False

    return user


async def create_token(user: _models.User):
    user_obj = User.from_orm(user)

    token = _jwt.encode(user_obj.dict(), JWT_SECRET)

    return dict(access_token=token, token_type="bearer")


async def get_current_user(
    db: _orm.Session = _fastapi.Depends(get_db),
    token: str = _fastapi.Depends(oauth2schema),
):
    try:
        payload = _jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(_models.User).get(payload["id"])
    except:
        raise _fastapi.HTTPException(
            status_code=401, detail="Invalid Email or Password"
        )

    return User.from_orm(user)


async def get_words(word: WordSearch,
    token: str = _fastapi.Depends(oauth2schema),):
    try:
        payload = _jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
   
    except:
         raise _fastapi.HTTPException(
            status_code=401, detail="Invalid Token"
        )

    return  {'words' : list(embeddings_dict.keys())}



async def get_vector(word: str,
    token: str = _fastapi.Depends(oauth2schema),):
    try:
        payload = _jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
       
    except:
         raise _fastapi.HTTPException(
            status_code=401, detail="Invalid Token"
        )

    return str(embeddings_dict[word])

async def find_similar_words(word: WordSearch,
    token: str = _fastapi.Depends(oauth2schema),):
    try:
        payload = _jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
       
    except:
         raise _fastapi.HTTPException(
            status_code=401, detail="Invalid Token"
        )

    def find_closest_embeddings(embedding):
            result = sorted(embeddings_dict.keys(), key=lambda word: spatial.distance.euclidean(embeddings_dict[word], embedding)) 
            return result
    print(word.word)
    return({'data' :find_closest_embeddings(embeddings_dict[word.word])[:word.limit]})

    
