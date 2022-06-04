from sqlalchemy import String, Integer, Column, UniqueConstraint, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from base import base

class Session(base):
    __tablename__ = 'Session'
    id = Column(Integer, primary_key=True)
    priceFilm = Column(Float, nullable=False)
    dateTimeStart = Column(DateTime, nullable=False)
    idShedule = Column(Integer, ForeignKey('Shedule.id', ondelete='CASCADE', onupdate='CASCADE'))
    shedule = relationship('Shedule')
    seats = relationship('Seat')