from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone

from app import models
from . import schemas
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .config import settings
from sqlalchemy.orm import Session
from .database import get_db



oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


#secret_key
#algorithm
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
#access_token_expire_minutes
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes



def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token, credentials_exception)

def require_pro(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_id = getattr(current_user, "id", None) or getattr(current_user, "user_id", None)
    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if user.subscription_status != "PRO":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="PRO subscription required to vote",
        )
    return user