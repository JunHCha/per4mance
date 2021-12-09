from typing import Optional

from fastapi.param_functions import Depends, Path, Query
from fastapi.routing import APIRouter
from starlette.responses import JSONResponse

from src.course.schemas import CoursePostSchema
from src.course.services import (
    create_course,
    create_coursexuser,
    delete_course,
    fetch_courses,
    update_course,
)
from src.models import User
from src.core.auth import get_current_user

router = APIRouter()


@router.get("/course")
async def get_courses(
    limit: Optional[int] = Query(10, ge=1),
    offset: Optional[int] = Query(0, ge=0),
    user: User = Depends(get_current_user),
) -> JSONResponse:
    """
    Fetch current managing/taking courses
    """
    courses = await fetch_courses(limit, offset, user=user)
    return JSONResponse(status_code=200, content=dict(data=courses))


@router.post("/course")
async def open_course(
    course_form: CoursePostSchema, evaluator: User = Depends(get_current_user)
) -> JSONResponse:
    """
    Open new course. Only evaluator can use this.
    """
    course = await create_course(course_info=course_form, user=evaluator)
    return JSONResponse(status_code=201, content=dict(course=course))


@router.patch("/course/{course_id}")
async def patch_course(
    course_form: CoursePostSchema,
    course_id: int = Path(1, description="Course id to update", ge=1),
    evaluator: User = Depends(get_current_user),
) -> JSONResponse:
    """
    Update course info.
    """
    course = await update_course(
        course_id=course_id, course_info=course_form, user=evaluator
    )
    return JSONResponse(status_code=200, content=dict(course=course))


@router.delete("/course/{course_id}")
async def close_course(
    course_id: int = Path(1, description="Course id to close", ge=1),
    evaluator: User = Depends(get_current_user),
) -> JSONResponse:
    """
    Delete the course. Only owner of the course can delete the course.
    """
    await delete_course(course_id, evaluator)
    return JSONResponse(status_code=200, content=dict(message="success"))


@router.post("/course/{course_id}/users/{user_id}")
async def add_student_to_course(
    course_id: int = Path(1, description="Course id to add student", ge=1),
    user_id: int = Path(1, description="Student's user id to add", ge=1),
    evaluator: User = Depends(get_current_user),
) -> JSONResponse:
    """
    Enroll student to course. Only owner of the course can add students.
    """
    course, student = await create_coursexuser(course_id, user_id, evaluator)
    return JSONResponse(status_code=201, content=dict(course=course, student=student))
