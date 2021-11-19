from sqlalchemy import Column, VARCHAR, Integer, DATE

from project.core.models import Base


class Picu_tbl(Base):
    __tablename__ = "picu_tbl"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DATE, nullable=False)
    description = Column(VARCHAR(255), nullable=False)
    user_email = Column(VARCHAR(255), nullable=False)
