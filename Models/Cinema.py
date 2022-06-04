from sqlalchemy import String, Integer, Column, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from base import base

class Cinema(base):
    __tablename__ = 'Cinema'
    id = Column(Integer, primary_key=True)
    street = Column(String(30), nullable=False)
    idCity = Column(Integer, ForeignKey('City.id', ondelete='CASCADE', onupdate='CASCADE'))
    city = relationship('City')
    halls = relationship('Hall')