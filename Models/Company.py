from sqlalchemy import String, Integer, Column
from sqlalchemy.orm import relationship
from base import base

class Company(base):
    __tablename__ = 'Company'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    country = Column(String(20), nullable=False)
    yearOfEstablishment = Column(Integer, nullable=False)
    films = relationship('Film')