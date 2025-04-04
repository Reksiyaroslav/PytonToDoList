import jwt
import datetime 
from fastapi import Depends 
from fastapi.security import OAuth2PasswordBearer
from typing import Dict
from sqlalchemy.orm import Session

from app.db.engine import User
from app.utils.utils import get_db
import secrets
import string

alphabet = string.ascii_letters + string.digits  # Буквы и цифры




oauth2_scheme =OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = ''.join(secrets.choice(alphabet) for _ in range(32)) 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
def create_jwt_token(data:Dict):
    to_encode = data.copy()
    expire = datetime.datetime.now()+datetime.timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
def  decode_jwt_tocen(token: str= Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}
def get_user_from_db(username:str,db:Session = next(get_db())):
    return db.query(User).filter(User.username==username).first()
