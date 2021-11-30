from fastapi.param_functions import Depends
from fastapi.routing import APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from per4mance.models import User
from per4mance.user.auth import get_current_user
from per4mance.user.schemas import SignUp, SignIn
from starlette.responses import JSONResponse
from per4mance.user.services import create_account, refresh_token

router = APIRouter()


@router.post("/users/sign-up")
async def signup(signup_form: SignUp):
    token = await create_account(signup_form)
    return JSONResponse(status_code=201, content=dict(token=token))


@router.post("/users/login")
async def login(signin_form: OAuth2PasswordRequestForm = Depends()):
    token = await refresh_token(signin_form)
    return JSONResponse(status_code=200, content=dict(token=token))


@router.get("/items")
async def get_item(current_user: User = Depends(get_current_user)):
    return JSONResponse(status_code=200, content="Hello world")
