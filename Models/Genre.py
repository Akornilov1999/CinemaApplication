from sqlalchemy import String, Integer, Column, UniqueConstraint
from sqlalchemy.orm import relationship
from base import base

class Genre(base):
    __tablename__ = 'Genre'
    id = Column(Integer, primary_key=True)
    name = Column(String(15), nullable=False)
    genrefilms = relationship('GenreFilm')
    __table_args__ = tuple(
        UniqueConstraint('name')
    )