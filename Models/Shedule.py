from sqlalchemy import String, Integer, Column, UniqueConstraint, ForeignKey, Date
from sqlalchemy.orm import relationship
from base import base

class Shedule(base):
    __tablename__ = 'Shedule'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    idFilm = Column(Integer, ForeignKey('Film.id', ondelete='CASCADE', onupdate='CASCADE'))
    film = relationship('Film')
    idHall = Column(Integer, ForeignKey('Hall.id', ondelete='CASCADE', onupdate='CASCADE'))
    hall = relationship('Hall')
    sessions = relationship('Session')