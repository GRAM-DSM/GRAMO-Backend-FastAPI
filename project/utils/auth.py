from fastapi import HTTPException, status

from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AccessTokenRequired, RefreshTokenRequired, JWTDecodeError

import bcrypt

from sqlalchemy.orm.session import Session

from project.core.models import Redis
from project.core.models.user import User_tbl


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
