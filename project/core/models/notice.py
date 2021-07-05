from sqlalchemy import Column, VARCHAR, Integer, DATETIME

from project.core.models import Base


class Notice_tbl(Base):
    __tablename__ = "notice_tbl"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(VARCHAR(50), nullable=False)
    content = Column(VARCHAR(1000), nullable=False)
    user_email = Column(VARCHAR(30), nullable=False)
    created_at = Column(DATETIME, nullable=False)
