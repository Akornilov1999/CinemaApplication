from sqlalchemy import String, Integer, Column, UniqueConstraint, Boolean, Date
from base import base

class Worker(base):
    __tablename__ = 'Worker'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    surname = Column(String(30), nullable=False)
    patronymic = Column(String(30), nullable=True)
    gender = Column(Boolean, nullable=False)
    dateBirthday = Column(Date, nullable=False)
    mail = Column(String(30), nullable=False)
    phone = Column(String(12), nullable=False)
    right = Column(String(20), nullable=False)
    seriesPassport = Column(String(4), nullable=False)
    numberPassport = Column(String(6), nullable=False)
    hashPassword = Column(String, nullable=False)
    saltPassword = Column(String, nullable=False)
    __table_args__ = tuple(
        UniqueConstraint('mail')
    )