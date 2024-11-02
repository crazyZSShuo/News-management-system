from fastapi import Body, FastAPI, Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from app.config.config import config
from app.curd.user import get_user_by_email, get_user_by_username, update_last_login, update_user, create_user
from app.models.users import User
from app.depends.db import get_db
from app.depends.security import create_token, verify_password
from app.schemas.users import Token, TokenRequest, UserCreate, UserInDB, UserUpdate
from jose import jwt
from app.depends.users import get_current_active_user

router_user = APIRouter()


@router_user.post("/register", response_model=UserInDB)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered."
        )

    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already  registered."
        )

    return create_user(db, user)


@router_user.post("/token", response_model=Token)
async def login(username: str = Body(...), password: str = Body(...), db: Session = Depends(get_db)):
    user: User = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    update_last_login(db, user.id)

    access_token = create_token(data={"sub": user.username})
    # refresh_token = create_token(data={"sub": user.username}, is_refresh=True)
    return {
        "access_token": access_token,
        # "refresh_token": refresh_token,
        "token_type": "bearer"
    }


# 刷新token 可有可无
@router_user.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: TokenRequest, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(refresh_token, config.app.SECRET_KEY, algorithms=[config.app.ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )
        username = payload.get("sub")
        user = get_user_by_username(db, username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        access_token = create_token(data={"sub": username})
        # new_refresh_token = create_token(data={"sub": username}, is_refresh=True)

        return {
            "access_token": access_token,
            # "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired",
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )


@router_user.get("/users/me", response_model=UserInDB)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router_user.put("/users/me", response_model=UserInDB)
async def update_user_me(user_update: UserUpdate, current_user: User = Depends(get_current_active_user),
                         db: Session = Depends(get_db)):
    updated_user = update_user(db, current_user.id, user_update)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not fount."
        )
    return updated_user


@router_user.get("/protected")
async def protected_router(current_user: User = Depends(get_current_active_user)):
    return {
        "message": f"Hello {current_user.username}",
        "email": current_user.email,
        "last_login": current_user.last_login
    }
