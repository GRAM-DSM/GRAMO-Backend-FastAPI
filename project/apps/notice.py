from fastapi import APIRouter, status, Depends

from fastapi_jwt_auth import AuthJWT

from pytz import timezone
from datetime import datetime

from project.core.schemas.notice import CreateNotice

from project.core.models import session
from project.core.models.notice import Notice_tbl

from project.utils import create, delete
from project.utils.auth import token_check
from project.utils.notice import get_notice_list, is_next_notice, is_notice, get_notice, is_own_notice
from project.utils.notify import get_user_fcm_tokens, send_message


router = APIRouter()


@router.post("/notice", status_code=status.HTTP_201_CREATED, tags=["notice"])
async def create_notice(body: CreateNotice, authorize: AuthJWT = Depends()):
    token_check(authorize=authorize, type="access")

    user_email = authorize.get_jwt_subject()

    create(
        cls=Notice_tbl,
        session=session,
        title=body.title,
        content=body.content,
        user_email=user_email,
        created_at=datetime.now(timezone("Asia/Seoul")).strftime("%Y-%m-%d %H:%M:%S")
    )

    tokens = get_user_fcm_tokens(session=session, email=user_email)
    send_message(tokens=tokens, title="새로운 공지사항", body=body.title)

    return {
        "message": "success"
    }


@router.get("/notice/list/{page}", status_code=status.HTTP_200_OK, tags=["notice"])
async def get_notices(page: int, authorize: AuthJWT = Depends()):
    token_check(authorize=authorize, type="access")

    limit = 10
    offset = page * limit

    notice_list = get_notice_list(session=session, limit=limit, offset=offset)
    is_next = is_next_notice(session=session, limit=limit, offset=offset)

    return {
       "notice": [{
           "id": notice.id,
           "title": notice.title,
           "content": notice.content,
           "user_name": user.name,
           "created_at": str(notice.created_at)
       } for notice, user in notice_list],
       "next_page": is_next
    }


@router.get("/notice/{notice_id}", status_code=status.HTTP_200_OK, tags=["notice"])
async def get_notice_detail(notice_id: int, authorize: AuthJWT = Depends()):
    token_check(authorize=authorize, type="access")

    is_notice(session=session, notice_id=notice_id)
    notice, user = get_notice(session=session, notice_id=notice_id)

    return {
       "notice": {
           "name": user.name,
           "created_at": str(notice.created_at),
           "title": notice.title,
           "content": notice.content
       }
   }


@router.delete("/notice/{notice_id}", status_code=status.HTTP_200_OK, tags=["notice"])
async def delete_one_notice(notice_id: int, authorize: AuthJWT = Depends()):
    token_check(authorize=authorize, type="access")

    notice = is_notice(session=session, notice_id=notice_id, return_it=True)

    email = authorize.get_jwt_subject()
    is_own_notice(notice=notice, email=email)

    delete(session=session, del_thing=notice)

    return {
        "message": "success"
    }
