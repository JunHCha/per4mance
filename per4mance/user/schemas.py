from pydantic import BaseModel


class SignUp(BaseModel):
    nickname: str
    account: str
    password: str
    is_evaluator: bool


class SignIn(BaseModel):
    account: str
    password: str
