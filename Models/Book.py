from sqlalchemy import String, Integer, Column, UniqueConstraint, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from base import base

class Book(base):
    __tablename__ = 'Book'
    id = Column(Integer, primary_key=True)
    dateTime = Column(DateTime, nullable=False)
    idSeat = Column(Integer, ForeignKey('Seat.id', ondelete='CASCADE', onupdate='CASCADE'))
    #seat = relationship('Seat')
    idClient = Column(Integer, ForeignKey('Client.id', ondelete='CASCADE', onupdate='CASCADE'))
    client = relationship('Client')