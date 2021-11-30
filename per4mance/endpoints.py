from typing import Optional

from fastapi.param_functions import Depends, Path, Query
from fastapi.routing import APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse

from per4mance.course.schemas import CoursePostSchema
from per4mance.course.services import create_course, delete_course, fetch_courses
from per4mance.models import User
from per4mance.user.auth import get_current_user
from per4mance.user.schemas import SignUp
from per4mance.user.services import create_account, refresh_token

router = APIRouter()


@router.post("/users/signup")
async def signup(signup_form: SignUp) -> JSONResponse:
    token = await create_account(signup_form)
    return JSONResponse(status_code=201, content=dict(token=token))


@router.post("/users/login")
async def login(signin_form: OAuth2PasswordRequestForm = Depends()) -> JSONResponse:
    token = await refresh_token(signin_form)
    return JSONResponse(
        status_code=200,
        content=dict(access_token=token, token_type="bearer"),
    )


@router.get("/course")
async def get_courses(
    limit: Optional[int] = Query(10, ge=1),
    offset: Optional[int] = Query(0, ge=0),
    user: User = Depends(get_current_user),
) -> JSONResponse:
    courses = await fetch_courses(limit, offset, user=user)
    return JSONResponse(status_code=200, content=dict(data=courses))


@router.post("/course")
async def open_course(
    course_form: CoursePostSchema, evaluator: User = Depends(get_current_user)
) -> JSONResponse:
    course = await create_course(course_info=course_form, user=evaluator)
    return JSONResponse(status_code=201, content=dict(course=course))


@router.delete("/course/{course_id}")
async def close_course(
    course_id: int = Path(1, description="Course id to close", ge=1),
    evaluator: User = Depends(get_current_user),
) -> JSONResponse:
    await delete_course(course_id, evaluator)
    return JSONResponse(status_code=200, content=dict(message="success"))
