from sqlalchemy import String, Integer, Column, UniqueConstraint
from sqlalchemy.orm import relationship
from base import base

class City(base):
    __tablename__ = 'City'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    cinemas = relationship('Cinema')
    __table_args__ = tuple(
        UniqueConstraint('name')
    )