from sqlalchemy import String, Integer, Column, UniqueConstraint, Boolean, Date
from sqlalchemy.orm import relationship
from base import base

class Client(base):
    __tablename__ = 'Client'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    surname = Column(String(30), nullable=False)
    patronymic = Column(String(30), nullable=True)
    gender = Column(Boolean, nullable=False)
    dateBirthday = Column(Date, nullable=False)
    mail = Column(String(30), nullable=False)
    phone = Column(String(12), nullable=False)
    hashPassword = Column(String, nullable=False)
    saltPassword = Column(String, nullable=False)
    books = relationship('Book')
    __table_args__ = tuple(
        UniqueConstraint('mail')
    )