from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import Optional
from app.depends.security import oauth2_scheme
from jose import JWTError, jwt
from app.config.config import config
from app.models.users import User
from app.depends.db import get_db


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # 获取当前用户
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.app.SECRET_KEY, algorithms=[config.app.ALGORITHM])
        username: str = payload.get("sub")
        if username is None or payload.get("type") != "access":
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user=Depends(get_current_user)):
    # 判断用户是否为激活状态
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not activate."
        )
    return current_user


async def get_super_user(current_user=Depends(get_current_active_user)):
    # 判断用户是否为管理员
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not super user"
        )
    return current_user


async def verify_authenticated_header(authenticated: Optional[str] = Header(None)):
    if not authenticated or authenticated.lower() != "true":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authenticated header is required",
        )
