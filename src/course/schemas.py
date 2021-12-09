import datetime

from pydantic import BaseModel


class CoursePostSchema(BaseModel):
    name: str
    start_term: datetime.date
    end_term: datetime.date
    description: str = ""
    survey_count: int = 4
    scale_factor: float = 0.2
