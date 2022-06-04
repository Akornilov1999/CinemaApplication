from sqlalchemy import String, Integer, Column, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from base import base

class Hall(base):
    __tablename__ = 'Hall'
    id = Column(Integer, primary_key=True)
    number = Column(String(20), nullable=False)
    idCinema = Column(Integer, ForeignKey('Cinema.id', ondelete='CASCADE', onupdate='CASCADE'))
    cinema = relationship('Cinema')
    idTypeOfHall = Column(Integer, ForeignKey('TypeOfHall.id', ondelete='CASCADE', onupdate='CASCADE'))
    typeOfHall = relationship('TypeOfHall')
    shedules = relationship('Shedule')
