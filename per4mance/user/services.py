import sqlalchemy as sa
import datetime

from fastapi import HTTPException

from per4mance import db_engine
from per4mance.core.utils import fetch_all
from per4mance.models import User
from per4mance.user.schemas import SignIn, SignUp
from per4mance.user.auth import fakehash, token_fake_encoder


async def create_account(signup_form: SignUp):
    nickname = signup_form.nickname
    account = signup_form.account
    password = fakehash(signup_form.password)
    is_evaluator = signup_form.is_evaluator
    created_at = datetime.date.today()

    is_duplicated = (
        len(fetch_all(sa.select([User.account]).where(User.account == account))) > 0
    ) or (len(fetch_all(sa.select([User.account]).where(User.account == account))) > 0)
    if is_duplicated:
        raise HTTPException(status_code=400, detail="duplicated account or nickname.")

    query = sa.insert(User).values(
        name=nickname,
        account=account,
        password=password,
        is_evaluator=is_evaluator,
        created_at=created_at,
    )
    token = dict(Authorization=f"Bearer {token_fake_encoder(account, password)}")
    with db_engine.connect() as conn:
        conn.execute(query)
        conn.commit()
    return token


async def refresh_token(signin_form: SignIn):
    query = sa.select(
        [
            User.account,
            User.password,
        ]
    ).where(User.account == signin_form.account)

    user = fetch_all(query)[0]
    if len(user) == 0:
        raise HTTPException(status_code=401, detail="no such account")

    is_verified = user["password"] == fakehash(signin_form.password)
    if is_verified:
        token = token_fake_encoder(signin_form.account, signin_form.password)
        return token
    else:
        raise HTTPException(status_code=401, detail="wrong password")
