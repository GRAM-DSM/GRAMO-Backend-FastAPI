from fastapi import HTTPException, status

from sqlalchemy.orm.query import Query
from sqlalchemy.orm.session import Session

from project.core.models.notice import Notice_tbl
from project.core.models.user import User_tbl


def get_notice_list(session: Session, limit: int, offset: int):
    notice_list = session.query(Notice_tbl, User_tbl) \
        .filter(Notice_tbl.user_email == User_tbl.email) \
        .order_by(Notice_tbl.created_at.desc()) \
        .limit(limit).offset(offset)

    return notice_list


def get_notice(session: Session, notice_id: int):
    joined_notice = session.query(Notice_tbl, User_tbl). \
        filter(Notice_tbl.user_email == User_tbl.email). \
        filter(Notice_tbl.id == notice_id)

    return joined_notice[0][0], joined_notice[0][1]


def is_next_notice(session: Session, limit: int, offset: int):
    next_notice = session.query(Notice_tbl).limit(1).offset(offset + limit).scalar()

    return True if next_notice else False


def is_notice(session: Session, notice_id: int, return_it = False):
    notice = session.query(Notice_tbl).filter(Notice_tbl.id == notice_id)

    if not notice.scalar():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="could not find notice matching this id")

    if return_it:
        return notice.first()


def is_own_notice(notice: Query, email: str):
    if not notice.user_email == email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="could not delete notice created by others")
