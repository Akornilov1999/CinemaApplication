from sqlalchemy import insert
from declaration import engine
from Models.Company import Company
from Models.Film import Film
from Models.Genre import Genre
from Models.GenreFilm import GenreFilm

with engine.connect() as conn:
    conn.execute(
        insert(Company),
        [
            {'name': 'Company 1', 'country': 'Country 1', 'yearOfEstablishment': 1995},
            {'name': 'Company 2', 'country': 'Country 2', 'yearOfEstablishment': 1996},
            {'name': 'Company 3', 'country': 'Country 3', 'yearOfEstablishment': 1997},
            {'name': 'Company 4', 'country': 'Country 4', 'yearOfEstablishment': 1998},
            {'name': 'Company 5', 'country': 'Country 5', 'yearOfEstablishment': 1999},
            {'name': 'Company 6', 'country': 'Country 6', 'yearOfEstablishment': 2001},
            {'name': 'Company 7', 'country': 'Country 7', 'yearOfEstablishment': 2002},
            {'name': 'Company 8', 'country': 'Country 8', 'yearOfEstablishment': 2004},
        ]
    )
    conn.execute(
        insert(Film),
        [
            {'name': 'Film 1', 'duration': '02:00:00', 'ageLimit': 18, 'idCompany': 1},
            {'name': 'Film 2', 'duration': '02:00:00', 'ageLimit': 16, 'idCompany': 2},
            {'name': 'Film 3', 'duration': '02:00:00', 'ageLimit': 16, 'idCompany': 1},
            {'name': 'Film 4', 'duration': '02:00:00', 'ageLimit': 12, 'idCompany': 3},
            {'name': 'Film 5', 'duration': '02:00:00', 'ageLimit': 12, 'idCompany': 5},
            {'name': 'Film 6', 'duration': '02:00:00', 'ageLimit': 16, 'idCompany': 1},
            {'name': 'Film 7', 'duration': '02:00:00', 'ageLimit': 12, 'idCompany': 4},
            {'name': 'Film 8', 'duration': '02:00:00', 'ageLimit': 12, 'idCompany': 3},
            {'name': 'Film 9', 'duration': '02:00:00', 'ageLimit': 18, 'idCompany': 7},
            {'name': 'Film 10', 'duration': '02:00:00', 'ageLimit': 16, 'idCompany': 7},
            {'name': 'Film 11', 'duration': '02:00:00', 'ageLimit': 18, 'idCompany': 6},
            {'name': 'Film 12', 'duration': '02:00:00', 'ageLimit': 12, 'idCompany': 8},

        ]
    )
    conn.execute(
        insert(Genre),
        [
            {'name': 'Жанр 1'}, {'name': 'Жанр 2'}, {'name': 'Жанр 3'}
        ]
    )
    conn.execute(
        insert(GenreFilm),
        [
            {'idGenre': 3, 'idFilm': 1}, {'idGenre': 2, 'idFilm': 2}, {'idGenre': 3, 'idFilm': 3},
            {'idGenre': 3, 'idFilm': 4}, {'idGenre': 1, 'idFilm': 5}, {'idGenre': 1, 'idFilm': 6},
            {'idGenre': 2, 'idFilm': 7}, {'idGenre': 3, 'idFilm': 8}, {'idGenre': 1, 'idFilm': 9},
            {'idGenre': 2, 'idFilm': 10}, {'idGenre': 2, 'idFilm': 11}, {'idGenre': 1, 'idFilm': 12}
        ]
    )
    conn.close()