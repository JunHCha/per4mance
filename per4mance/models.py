from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = sa.Column(UUID, primary_key=True)
    name = sa.Column(sa.String(30))
    company = sa.Column(sa.String(30))
    account = sa.Column(sa.String(200))
    password = sa.Column(sa.String(200))
    email_address = sa.Column(sa.String(200))
    is_evaluator = sa.Column(sa.BOOLEAN)
    created_at = sa.DateTime(timezone=True)
