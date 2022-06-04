from sqlalchemy import String, Integer, Column, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from base import base

class GenreFilm(base):
    __tablename__ = 'GenreFilm'
    id = Column(Integer, primary_key=True)
    idGenre = Column(Integer, ForeignKey('Genre.id', ondelete='CASCADE', onupdate='CASCADE'))
    genre = relationship('Genre')
    idFilm = Column(Integer, ForeignKey('Film.id', ondelete='CASCADE', onupdate='CASCADE'))
    film = relationship('Film')