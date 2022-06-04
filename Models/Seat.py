from sqlalchemy import String, Integer, Column, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from base import base

class Seat(base):
    __tablename__ = 'Seat'
    id = Column(Integer, primary_key=True)
    numberRow = Column(Integer, nullable=False)
    numberCol = Column(Integer, nullable=False)
    idSession = Column(Integer, ForeignKey('Session.id', ondelete='CASCADE', onupdate='CASCADE'))
    session = relationship('Session')
    idBook = Column(Integer, ForeignKey('Book.id', onupdate='CASCADE'), nullable=True)
    #book = relationship('Book')