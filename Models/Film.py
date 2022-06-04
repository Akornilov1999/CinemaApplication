from sqlalchemy import String, Integer, Column, UniqueConstraint, Time, ForeignKey
from sqlalchemy.orm import  relationship
from base import base

class Film(base):
    __tablename__ = 'Film'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    duration = Column(Time, nullable=False)
    ageLimit = Column(Integer, nullable=False)
    idCompany = Column(Integer, ForeignKey('Company.id', ondelete='CASCADE', onupdate='CASCADE'))
    company = relationship('Company')
    genreFilms = relationship('GenreFilm')
    shedules = relationship('Shedule')