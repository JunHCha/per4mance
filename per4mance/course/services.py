import datetime

import sqlalchemy as sa
from fastapi.exceptions import HTTPException

from per4mance import db_engine
from per4mance.core.utils import fetch_all
from per4mance.course.schemas import CoursePostSchema
from per4mance.models import Course, User


async def create_course(course_info: CoursePostSchema, user: User) -> None:
    if not user.is_evaluator:
        raise HTTPException(status_code=401, detail="only evaluator can open course.")
    if course_info.end_term < course_info.start_term:
        raise HTTPException(
            status_code=400, detail="start term can't be later than end date."
        )

    if (
        len(
            fetch_all(
                sa.select([Course.id]).where(
                    Course.name == course_info.name and Course.evaluator == user.id
                )
            )
        )
        > 0
    ):
        raise HTTPException(status_code=400, detail="already exist")

    now = datetime.datetime.now()

    query = sa.insert(Course).values(
        evaluator=user.id,
        name=course_info.name,
        start_term=course_info.start_term,
        end_term=course_info.end_term,
        description=course_info.description,
        created_at=now,
        updated_at=now,
    )
    with db_engine.connect() as conn:
        conn.execute(query)
        conn.commit()

    course = fetch_all(
        sa.select(
            [
                Course.id,
                Course.evaluator,
                Course.survey_config,
                Course.name,
                Course.start_term,
                Course.end_term,
                Course.description,
            ]
        ).where(Course.evaluator == user.id and Course.name == course_info.name)
    )[0]
    course["start_term"] = course["start_term"].strftime("%Y-%m-%d")
    course["end_term"] = course["end_term"].strftime("%Y-%m-%d")
    return course
