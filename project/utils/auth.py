from fastapi import HTTPException, status

from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AccessTokenRequired, RefreshTokenRequired, JWTDecodeError

import bcrypt

from sqlalchemy import or_
from sqlalchemy.orm.session import Session

from project.core.models import Redis
from project.core.models.user import User_tbl
from project.core.models.notice import Notice_tbl
from project.core.models.homework import Homework_tbl
from project.core.models.picu import Picu_tbl

from project.utils import delete


def is_user(session: Session, email: str, return_it = False):
    user = session.query(User_tbl).filter(User_tbl.email == email)

    if user.scalar():
        if return_it:
            return user.first()

        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="this email is already in use")

    if return_it:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="could not find user matching this token")


def user_authentication(session: Session, email: str, password: str):
    user = session.query(User_tbl).filter(User_tbl.email == email)

    if not user.scalar():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="email and password does not match")

    user = user.first()

    check_user_pw = bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8"))
    if not check_user_pw:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="email and password does not match")

    return user


def refresh_token_validation(email: str):
    token = Redis.get(email)

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not find user matching this token")


def token_check(authorize: AuthJWT, type: str):
    try:
        if type == "access":
            authorize.jwt_required()
        elif type == "refresh":
            authorize.jwt_refresh_token_required()
        else:
            raise ValueError
    except ValueError:
        raise ValueError
    except AccessTokenRequired:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="access token required")
    except RefreshTokenRequired:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="refresh token required")
    except JWTDecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token has expired")


def init_withdrawal(session: Session, email: str):
    for notice in session.query(Notice_tbl).filter(Notice_tbl.user_email == email).all():
        session.delete(notice)

    for homework in session.query(Homework_tbl)\
        .filter(or_(Homework_tbl.teacher_email == email, Homework_tbl.student_email == email)).all():
        session.delete(homework)

    for picu in session.query(Picu_tbl).filter(Picu_tbl.user_email == email).all():
        session.delete(picu)
