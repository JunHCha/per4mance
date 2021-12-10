import sqlalchemy as sa
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordBearer

from per4mance.core.utils import fetch_all
from per4mance.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


def fakehash(password: str) -> str:
    return "fakehash_" + password


def token_fake_encoder(username: str) -> str:
    return "fakeencoded_" + username


def token_fake_decoder(token: str) -> str:
    signin_info = token.split("fakeencoded_")

    account = signin_info[1]
    return account


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    account = token_fake_decoder(token)
    user_dict = await fetch_all(
        sa.select([col for col in User.__table__.columns]).where(
            User.account == account
        )
    )[0]
    user = User(
        id=user_dict["id"],
        name=user_dict["name"],
        company=user_dict["company"],
        account=user_dict["account"],
        password=user_dict["password"],
        email_address=user_dict["email_address"],
        is_evaluator=user_dict["is_evaluator"],
        created_at=user_dict["created_at"],
    )
    return user
