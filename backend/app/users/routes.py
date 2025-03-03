from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from .auth import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_current_active_user
from .utils import get_password_hash, validate_email
from .serializers import User, Token
from .auth import db
from .models import UserInDB

router = APIRouter()

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@router.get("/users", response_model=list[User])
async def get_users():
    users = []
    for i in db.query(UserInDB).all():
        user = User(username=i.username, email=i.email, password=i.hashed_password)
        users.append(user)
    return users


@router.post("/users")
async def create_user(user: User = None):
    username = user.username
    email = user.email
    password = user.password
    credentials_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Not valid credentials",
    )
    hashed_password = get_password_hash(password)
    if not validate_email(email):
        raise credentials_exception

    user = UserInDB(username=username, email=email, hashed_password=hashed_password, disabled=False)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]