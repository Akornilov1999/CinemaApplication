from PyQt5 import QtWidgets
from declaration import engine
from WorkersWidget.GenreFilmsWidget.AddGenreFilmDialog import AddGenreFilmDialog
from WorkersWidget.GenreFilmsWidget.ChangeGenreFilmDialog import ChangeGenreFilmDialog
from sqlalchemy import select, func, insert, update, delete
from Models.Film import Film
from Models.Genre import Genre
from Models.GenreFilm import GenreFilm

class GenreFilmsWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(GenreFilmsWidget, self).__init__(*args, **kwargs)
        self.addButton = QtWidgets.QPushButton('Добавить')
        self.addButton.clicked.connect(self.addButtonClicked)
        self.changeButton = QtWidgets.QPushButton('Изменить')
        self.changeButton.clicked.connect(self.changeButtonClicked)
        self.deleteButton = QtWidgets.QPushButton('Удалить')
        self.deleteButton.clicked.connect(self.deleteButtonClicked)
        self.hBoxLayout = QtWidgets.QHBoxLayout()
        self.hBoxLayout.addWidget(self.addButton)
        self.hBoxLayout.addWidget(self.changeButton)
        self.hBoxLayout.addWidget(self.deleteButton)
        self.widgetWithButtons = QtWidgets.QWidget()
        self.widgetWithButtons.setLayout(self.hBoxLayout)
        self.vBoxLayout = QtWidgets.QVBoxLayout()
        self.listOfGenreFilms = QtWidgets.QTableWidget()
        self.listOfGenreFilms.setEditTriggers(self.listOfGenreFilms.EditTrigger.NoEditTriggers)
        self.listOfGenreFilms.setSelectionMode(self.listOfGenreFilms.SelectionMode.SingleSelection)
        self.listOfGenreFilms.setSelectionBehavior(self.listOfGenreFilms.SelectionBehavior.SelectRows)
        self.listOfGenreFilms.setColumnCount(2)
        self.listOfGenreFilms.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem('Фильм'))
        self.listOfGenreFilms.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem('Жанр'))
        self.listOfGenreFilms.pressed.connect(self.changeEnableButtons)
        self.vBoxLayout.addWidget(self.listOfGenreFilms)
        self.vBoxLayout.addWidget(self.widgetWithButtons)
        self.setLayout(self.vBoxLayout)
        self.updateData()

    def updateData(self):
        self.listOfGenreFilms.setRowCount(0)
        with engine.connect() as conn:
            index = 0
            query = (select(GenreFilm.id, GenreFilm.idFilm, GenreFilm.idGenre, Film.name, Genre.name)
                     .join(Film, Film.id == GenreFilm.idFilm)
                     .join(Genre, Genre.id == GenreFilm.idGenre)
                     .order_by(Film.name, Genre.name))
            for row in conn.execute(query):
                item = QtWidgets.QTableWidgetItem(row[3])
                item.setData(1, row[1])
                item.setData(3, row[0])
                self.listOfGenreFilms.insertRow(index)
                self.listOfGenreFilms.setItem(index, 0, item)
                item1 = QtWidgets.QTableWidgetItem(row[4])
                item1.setData(1, row[2])
                self.listOfGenreFilms.setItem(index, 1, item1)
                index += 1
            self.addButton.setEnabled(False)\
                if len(conn.execute(select(Film)).all()) == 0 or len(conn.execute(select(Genre)).all()) == 0\
                else self.addButton.setEnabled(True)
            conn.close()
        self.changeEnableButtons()

    def addButtonClicked(self):
        query = (select(Film.id, Film.name).order_by(Film.name))
        query1 = (select(Genre.id, Genre.name).order_by(Genre.name))
        listOfFilms = []
        with engine.connect() as conn:
            for row in conn.execute(query):
                listOfFilms.append((row[0], row[1]))
            conn.close()
        listOfGenres = []
        with engine.connect() as conn:
            for row in conn.execute(query1):
                listOfGenres.append((row[0], row[1]))
            conn.close()
        self.addGenreFilmDialog = AddGenreFilmDialog(listOfFilms, listOfGenres)
        while True:
            self.addGenreFilmDialog.listOfFilms.setEnabled(True)
            self.addGenreFilmDialog.exec()
            if self.addGenreFilmDialog.listOfFilms.isEnabled():
                break
            else:
                query = (select(func.count())
                         .where(GenreFilm.idFilm == self.addGenreFilmDialog.listOfFilms.itemData
                (self.addGenreFilmDialog.listOfFilms.currentIndex(), 1))
                         .where(GenreFilm.idGenre == self.addGenreFilmDialog.listOfGenres.itemData
                (self.addGenreFilmDialog.listOfGenres.currentIndex(), 1)))
                with engine.connect() as conn:
                    if conn.execute(query).all()[0][0] > 0:
                        messageBox = QtWidgets.QMessageBox()
                        messageBox.setWindowTitle('Ошибка')
                        messageBox.addButton('Ок', 5)
                        messageBox.setText('Такая связка уже существует!')
                        messageBox.exec()
                        conn.close()
                    else:
                        conn.execute(
                            insert(GenreFilm),
                            [
                                {'idGenre': self.addGenreFilmDialog.listOfGenres.itemData(
                                     self.addGenreFilmDialog.listOfGenres.currentIndex(), 1),
                                 'idFilm': self.addGenreFilmDialog.listOfFilms.itemData(
                                     self.addGenreFilmDialog.listOfFilms.currentIndex(), 1)},
                            ]
                        )
                        conn.close()
                        self.updateData()
                        break

    def changeButtonClicked(self):
        if len(self.listOfGenreFilms.selectedItems()) == 2:
            query = (select(Film.id, Film.name).order_by(Film.name))
            query1 = (select(Genre.id, Genre.name).order_by(Genre.name))
            listOfFilms = []
            with engine.connect() as conn:
                for row in conn.execute(query):
                    listOfFilms.append((row[0], row[1]))
                conn.close()
            listOfGenres = []
            with engine.connect() as conn:
                for row in conn.execute(query1):
                    listOfGenres.append((row[0], row[1]))
                conn.close()
            self.changeGenreFilmDialog = ChangeGenreFilmDialog(
                listOfFilms, listOfGenres,
                self.listOfGenreFilms.item(self.listOfGenreFilms.currentRow(), 0).data(1),
                self.listOfGenreFilms.item(self.listOfGenreFilms.currentRow(), 1).data(1))
            while True:
                self.changeGenreFilmDialog.listOfFilms.setEnabled(True)
                self.changeGenreFilmDialog.exec()
                if self.changeGenreFilmDialog.listOfFilms.isEnabled():
                    break
                else:
                    with engine.connect() as conn:
                        if len(conn.execute(select(GenreFilm).where(GenreFilm.id != self.listOfGenreFilms
                                                                 .item(self.listOfGenreFilms.currentRow(), 0).data(3))
                                     .where(GenreFilm.idFilm == self.changeGenreFilmDialog.listOfFilms
                                            .itemData(self.changeGenreFilmDialog.listOfFilms.currentIndex(), 1))
                                     .where(GenreFilm.idGenre == self.changeGenreFilmDialog.listOfGenres
                                .itemData(self.changeGenreFilmDialog.listOfGenres.currentIndex(), 1))).all()) > 0:
                            messageBox = QtWidgets.QMessageBox()
                            messageBox.setWindowTitle('Ошибка')
                            messageBox.addButton('Ок', 5)
                            messageBox.setText('Такая связка уже существует!')
                            messageBox.exec()
                            conn.close()
                        else:
                            conn.execute(
                                update(GenreFilm)
                                    .values(idGenre=self.changeGenreFilmDialog.listOfGenres.itemData(
                                                self.changeGenreFilmDialog.listOfGenres.currentIndex(), 1),
                                            idFilm=self.changeGenreFilmDialog.listOfFilms.itemData(
                                                self.changeGenreFilmDialog.listOfFilms.currentIndex(), 1))
                                    .where(GenreFilm.id == self.listOfGenreFilms.item
                                (self.listOfGenreFilms.currentRow(), 0).data(3))
                            )
                            conn.close()
                            self.updateData()
                            break

    def deleteButtonClicked(self):
        if self.listOfGenreFilms.currentRow() > -1:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setWindowTitle('Удаление связки')
            messageBox.addButton('Удалить', 5)
            messageBox.addButton('Отменить', 6)
            messageBox.setText('Удалить связку \"'
                               + self.listOfGenreFilms.item(self.listOfGenreFilms.currentRow(), 0).text()
                               + '-' + self.listOfGenreFilms.item(self.listOfGenreFilms.currentRow(), 1).text() + '\"?')
            reply = messageBox.exec()
            if reply == 0:
                with engine.connect() as conn:
                    query = (select(func.count())
                             .where(GenreFilm.id ==
                                    self.listOfGenreFilms.item(self.listOfGenreFilms.currentRow(), 0).data(3)))
                    if conn.execute(query).all()[0][0] != 1:
                        messageBox = QtWidgets.QMessageBox()
                        messageBox.setWindowTitle('Ошибка')
                        messageBox.addButton('Ок', 5)
                        messageBox.setText('Связки \"'
                                           + self.listOfGenreFilms.item(self.listOfGenreFilms.currentRow(), 0).text()
                                           + '-'
                                           + self.listOfGenreFilms.item(self.listOfGenreFilms.currentRow(), 1).text()
                                           + '\" не существует!')
                        messageBox.exec()
                        conn.close()
                    else:
                        conn.execute(
                            delete(GenreFilm)
                                .where(GenreFilm.id == self.listOfGenreFilms.item
                            (self.listOfGenreFilms.currentRow(), 0).data(3))
                        )
                        conn.close()
                        self.updateData()

    def changeEnableButtons(self):
        if len(self.listOfGenreFilms.selectedItems()) != 2:
            self.changeButton.setEnabled(False)
            self.deleteButton.setEnabled(False)
        else:
            self.changeButton.setEnabled(True)
            self.deleteButton.setEnabled(True)