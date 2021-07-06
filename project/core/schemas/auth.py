from pydantic import BaseModel, EmailStr, constr, conint

from enum import Enum

class MajorEnum(str, Enum):
    android = "ANDROID"
    ios = "IOS"
    backend = "BACKEND"
    design = "DESIGN"


class Signup(BaseModel):
    email: EmailStr
    password: constr(min_length=5, max_length=20)
    name: constr(min_length=1)
    major: MajorEnum


class SendEmail(BaseModel):
    email: EmailStr


class CheckCode(BaseModel):
    email: EmailStr
    code: conint(gt=99999, lt=1000000)


class Login(BaseModel):
    email: EmailStr
    password: constr(min_length=5, max_length=20)
    token: str
