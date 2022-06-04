from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists
from base import base
from Models.Book import Book
from Models.Cinema import Cinema
from Models.City import City
from Models.Client import Client
from Models.Company import Company
from Models.Film import Film
from Models.Genre import Genre
from Models.GenreFilm import GenreFilm
from Models.Hall import Hall
from Models.Seat import Seat
from Models.Session import Session
from Models.Shedule import Shedule
from Models.TypeOfHall import TypeOfHall
from Models.Worker import Worker

engine = create_engine('postgresql://postgres:passwd@localhost:5432/CinemaDB')
if not database_exists(engine.url):
    create_database(engine.url)
    base.metadata.create_all(engine)
else:
    base.metadata.create_all(engine)