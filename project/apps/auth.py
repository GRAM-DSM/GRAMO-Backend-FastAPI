from fastapi import APIRouter, status, Depends

from fastapi_jwt_auth import AuthJWT

import bcrypt

from datetime import timedelta

import random

from project.core.schemas.auth import Signup, Login, SendEmail, CheckCode

from project.core.models import session, Redis
from project.core.models.user import User_tbl

from project.utils import create, delete
from project.utils.auth import is_user, user_authentication, refresh_token_validation, token_check
from project.utils.email import send_code, code_check
from project.utils.notify import set_user_fcm_token

from project.config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES, ALGORITHM


router = APIRouter()


@router.post("/signup", status_code=status.HTTP_201_CREATED, tags=["auth"])
async def signup(body: Signup):
    is_user(session=session, email=body.email)

    create(
        cls=User_tbl,
        session=session,
        email=body.email,
        password=bcrypt.hashpw(body.password.encode("utf-8"), bcrypt.gensalt()),
        name=body.name,
        major=body.major,
        email_status=1
    )

    return {
        "message": "success"
    }


@router.post("/sendemail", status_code=status.HTTP_200_OK, tags=["auth"])
async def send_email(body: SendEmail):
    is_user(session=session, email=body.email)

    code = f"{random.randint(111111, 999999):04d}"

    await send_code(code=code, address=body.email)

    Redis.setex(name=body.email, value=code, time=timedelta(minutes=3))

    return {
               "message": "success"
           }


@router.post("/checkcode", status_code=status.HTTP_200_OK, tags=["auth"])
async def authenticate_email_code(body: CheckCode):
    code_check(email=body.email, code=body.code)

    return {
        "message": "success"
    }


@router.post("/auth", status_code=status.HTTP_200_OK, tags=["auth"])
async def login(body: Login, authorize: AuthJWT = Depends()):
    user = user_authentication(session=session, email=body.email, password=body.password)

    set_user_fcm_token(session=session, token=body.token, email=body.email)

    access_expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_expires_delta = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    access_token = authorize.create_access_token(
        subject=body.email,
        algorithm=ALGORITHM,
        expires_time=access_expires_delta
    )
    refresh_token = authorize.create_refresh_token(
        subject=body.email,
        algorithm=ALGORITHM,
        expires_time=refresh_expires_delta
    )

    Redis.setex(name=body.email,
                value=refresh_token,
                time=refresh_expires_delta)

    return {
        "name": user.name,
        "major": user.major,
        "access_token": access_token,
        "refresh_token": refresh_token
    }


@router.get("/auth", status_code=status.HTTP_201_CREATED, tags=["auth"])
async def refresh_token(authorize: AuthJWT = Depends()):
    token_check(authorize=authorize, type="refresh")

    email = authorize.get_jwt_subject()
    refresh_token_validation(email=email)

    access_expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = authorize.create_access_token(
        subject=email,
        algorithm=ALGORITHM,
        expires_time=access_expires_delta
    )

    return {
        "access_token": access_token
    }


@router.delete("/auth", status_code=status.HTTP_200_OK, tags=["auth"])
async def logout(authorize: AuthJWT = Depends()):
    token_check(authorize=authorize, type="access")

    email = authorize.get_jwt_subject()
    refresh_token_validation(email=email)

    Redis.delete(email)

    return {
        "message": "success"
    }


@router.delete("/withdrawal", status_code=status.HTTP_200_OK, tags=["auth"])
async def withdrawal(authorize: AuthJWT = Depends()):
    token_check(authorize=authorize, type="access")

    email = authorize.get_jwt_subject()
    user = is_user(session=session, email=email, return_it=True)
    delete(session=session, del_thing=user)

    return {
        "message": "success"
    }
