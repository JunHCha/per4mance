from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordBearer

from per4mance.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


def fakehash(password: str):
    return "fakehash_" + password


def token_fake_encoder(account: str, password: str):
    return "fakeencoded_" + account + "fakeencoded_" + password


def token_fake_decoder(token: str):
    signin_info = token.split("fakeecoded_")
    account = signin_info[0]
    password = signin_info[0]
    return (account, password)


def get_current_user(token: str = Depends(oauth2_scheme)):
    decoded = token_fake_decoder(token)
    user = User(account=decoded[0], password="fakeencoded_" + decoded[1])
    return user
