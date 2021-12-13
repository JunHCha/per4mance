from datetime import datetime, timedelta
from typing import Dict, Optional

import sqlalchemy as sa
from fastapi import HTTPException
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext

from per4mance.config import SECRET_KEY
from per4mance.core.utils.db import fetch_one
from per4mance.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def fakehash(password: str) -> str:
    return "fakehash_" + password


def token_fake_encoder(username: str) -> str:
    return "fakeencoded_" + username


def token_fake_decoder(token: str) -> str:
    signin_info = token.split("fakeencoded_")

    account = signin_info[1]
    return account


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms="HS256")
        account = payload.get("sub")
        if account is None:
            raise HTTPException(status_code=401, detail="invalid credential")
    except JWTError:
        raise HTTPException(status_code=401, detail="invalid credential")

    account = token_fake_decoder(token)
    user = await fetch_one(
        sa.select([col for col in User.__table__.columns]).where(
            User.account == account
        )
    )
    user = User(
        id=user["id"],
        name=user["name"],
        company=user["company"],
        account=user["account"],
        password=user["password"],
        email_address=user["email_address"],
        is_evaluator=user["is_evaluator"],
        created_at=user["created_at"],
    )
    if user is None:
        raise HTTPException(status_code=401, detail="invalid credential")
    return user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    data: dict, expires: Optional[timedelta] = timedelta(days=14)
) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt


async def refresh_token(signin_form: OAuth2PasswordRequestForm) -> Dict[str, str]:
    query = sa.select(
        [
            User.account,
            User.password,
        ]
    ).where(User.account == signin_form.username)

    user = await fetch_one(query)
    if user is None:
        raise HTTPException(status_code=401, detail="invalid account")

    verified = verify_password(signin_form.password, user["password"])

    if not verified:
        raise HTTPException(status_code=401, detail="wrong password")
    else:
        token = create_access_token(
            data={"sub": signin_form.username}, expires=timedelta(days=14)
        )
        return {"access_tokens": token, "token_type": "bearer"}
