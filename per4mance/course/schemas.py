import datetime

from pydantic import BaseModel


class CoursePostSchema(BaseModel):
    name: str
    start_term: datetime.date
    end_term: datetime.date
    description: str = ""
