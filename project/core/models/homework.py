from sqlalchemy import Column, VARCHAR, Integer, DATE, BINARY

from project.core.models import Base


class Homework_tbl(Base):
    __tablename__ = "homework_tbl"

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(VARCHAR(255), nullable=False)
    major = Column(VARCHAR(255), nullable=False)
    is_rejected = Column(BINARY(1), nullable=False)
    is_submitted = Column(BINARY(1), nullable=False)
    student_email = Column(VARCHAR(255), nullable=False)
    teacher_email = Column(VARCHAR(255), nullable=False)
    end_date = Column(DATE, nullable=False)
    start_date = Column(DATE, nullable=False)
    title = Column(VARCHAR(255), nullable=False)
