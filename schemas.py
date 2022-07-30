import datetime as _dt
import pydantic as _pydantic

from typing import Union

class _UserBase(_pydantic.BaseModel):
    email : str

class UserCreate(_UserBase):
    hashed_password: str

    class Config:
        orm_mode = True

class User(_UserBase):
    id: int

    class Config:
        orm_mode = True


class WordSearch(_pydantic.BaseModel):
    word: Union[str, None] = None
    limit : Union[int, None] = None



