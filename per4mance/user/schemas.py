from pydantic import BaseModel


class SignUp(BaseModel):
    name: str
    account: str
    password: str
    is_evaluator: bool = False
