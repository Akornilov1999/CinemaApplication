from sqlalchemy import String, Integer, Column, UniqueConstraint
from sqlalchemy.orm import relationship
from base import base

class TypeOfHall(base):
    __tablename__ = 'TypeOfHall'
    id = Column(Integer, primary_key=True)
    type = Column(String(20), nullable=False)
    countRow = Column(Integer, nullable=False)
    countCol = Column(Integer, nullable=False)
    halls = relationship('Hall')