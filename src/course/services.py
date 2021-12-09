import datetime
from typing import Any, Dict, List, Tuple

import sqlalchemy as sa
from fastapi.exceptions import HTTPException

from src import db_engine
from src.core.utils import fetch_all
from src.course.schemas import CoursePostSchema
from src.models import Course, CourseXStudent, User


async def fetch_courses(limit: int, offset: int, user: User) -> None:
    if user.is_evaluator:
        query = (
            sa.select([col for col in Course.__table__.columns])
            .where(Course.evaluator == user.id)
            .limit(limit)
            .offset(offset)
        )
    else:
        course_query = sa.select([CourseXStudent.course]).where(
            CourseXStudent.student == user.id
        )
        query = (
            sa.select([col for col in Course.__table__.columns])
            .where(Course.id.in_(course_query.as_scalar()))
            .limit(limit)
            .offset(offset)
        )

    courses = fetch_all(query)
    return courses


async def create_course(
    course_info: CoursePostSchema, user: User
) -> List[Dict[str, Any]]:
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
                    (Course.name == course_info.name) & (Course.evaluator == user.id)
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
        survey_count=course_info.survey_count,
        scale_factor=course_info.scale_factor,
        created_at=now,
        updated_at=now,
    )
    with db_engine.connect() as conn:
        conn.execute(query)
        conn.commit()

    course = fetch_all(
        sa.select([col for col in Course.__table__.columns]).where(
            (Course.evaluator == user.id) & (Course.name == course_info.name)
        )
    )[0]
    return course


async def update_course(
    course_id: int, course_info: CoursePostSchema, user: User
) -> List[Dict[str, Any]]:
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
                    (Course.name == course_info.name) & (Course.evaluator == user.id)
                )
            )
        )
        > 0
    ):
        raise HTTPException(status_code=400, detail="already exist")

    now = datetime.datetime.now()
    query = (
        sa.update(Course)
        .where(Course.id == course_id)
        .values(
            evaluator=user.id,
            name=course_info.name,
            start_term=course_info.start_term,
            end_term=course_info.end_term,
            description=course_info.description,
            survey_count=course_info.survey_count,
            scale_factor=course_info.scale_factor,
            updated_at=now,
        )
    )
    with db_engine.connect() as conn:
        conn.execute(query)
        conn.commit()

    course = fetch_all(
        sa.select([col for col in Course.__table__.columns]).where(
            (Course.evaluator == user.id) & (Course.name == course_info.name)
        )
    )[0]
    return course


async def delete_course(course_id: int, user: User) -> None:
    if not user.is_evaluator:
        raise HTTPException(status_code=401, detail="only evaluator can delete course.")

    target = fetch_all(
        sa.select([Course.id, Course.evaluator]).where(Course.id == course_id)
    )
    if len(target) == 0:
        raise HTTPException(status_code=404, detail="course not found")
    if target[0]["evaluator"] != user.id:
        raise HTTPException(
            status_code=401, detail="'cannot delete other users' course"
        )

    query = sa.delete(Course).where(Course.id == course_id)
    with db_engine.connect() as conn:
        conn.execute(query)
        conn.commit()


async def create_coursexuser(
    course_id: int, student_id: int, user: User
) -> Tuple[Any, Any]:
    if not user.is_evaluator:
        raise HTTPException(
            status_code=401, detail="only evaluator can manage students"
        )

    course = fetch_all(
        sa.select([col for col in Course.__table__.columns]).where(
            Course.id == course_id
        )
    )
    if len(course) == 0:
        raise HTTPException(status_code=404, detail="course not found")
    if course[0]["evaluator"] != user.id:
        raise HTTPException(
            status_code=401, detail="cannot manage other evaluators' course"
        )

    user = fetch_all(
        sa.select([col for col in User.__table__.columns]).where(User.id == student_id)
    )
    if len(user) == 0:
        raise HTTPException(status_code=404, detail="user not found")
    if user[0]["is_evaluator"]:
        raise HTTPException(
            status_code=400, detail="cannot add an evaluator as a student"
        )

    coursexuser = fetch_all(
        sa.select([col for col in CourseXStudent.__table__.columns]).where(
            (CourseXStudent.course == course_id)
            & (CourseXStudent.student == student_id)
        )
    )
    if len(coursexuser) > 0:
        raise HTTPException(status_code=401, detail="duplicated values")

    query = sa.insert(CourseXStudent).values(course=course_id, student=student_id)
    with db_engine.connect() as conn:
        conn.execute(query)
        conn.commit()
    return (course, user)
