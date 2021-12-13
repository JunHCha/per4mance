import datetime
from typing import Dict

import sqlalchemy as sa
from fastapi import HTTPException

from per4mance import db_engine
from per4mance.core.utils.auth import create_access_token, pwd_context
from per4mance.core.utils.db import fetch_one
from per4mance.models import User
from per4mance.user.schemas import SignUp


async def create_account(signup_form: SignUp) -> Dict[str, str]:
    name = signup_form.name
    account = signup_form.account
    password = pwd_context.hash(signup_form.password)
    is_evaluator = signup_form.is_evaluator
    created_at = datetime.datetime.now()

    user_search = await fetch_one(
        sa.select([User.account]).where(User.account == account)
    )
    is_duplicated = user_search is not None

    if is_duplicated:
        raise HTTPException(status_code=400, detail="duplicated account or nickname.")

    query = sa.insert(User).values(
        account=account,
        name=name,
        password=password,
        is_evaluator=is_evaluator,
        created_at=created_at,
    )
    token = dict(Authorization=f"Bearer {create_access_token(data={'sub': account})}")

    async with db_engine.connect() as conn:
        await conn.execute(query)
        await conn.commit()
    return token
