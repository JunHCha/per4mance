from fastapi.param_functions import Depends
from fastapi.routing import APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse

from per4mance.core.utils.auth import refresh_token
from per4mance.user.schemas import SignUp
from per4mance.user.services import create_account

router = APIRouter()


@router.post("/users/signup")
async def signup_view(signup_form: SignUp) -> JSONResponse:
    """
    Create account
    """
    token = await create_account(signup_form)
    return JSONResponse(status_code=201, content=dict(token=token))


@router.post("/users/login")
async def signin_view(
    signin_form: OAuth2PasswordRequestForm = Depends(),
) -> JSONResponse:
    """
    Get fresh token about requested user info.
    """
    token = await refresh_token(signin_form)
    return JSONResponse(status_code=200, content=token)
