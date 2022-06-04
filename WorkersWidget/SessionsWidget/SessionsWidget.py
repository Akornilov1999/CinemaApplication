from PyQt5 import QtWidgets
from datetime import datetime, date, time
from declaration import engine
from WorkersWidget.SessionsWidget.AddSessionDialog import AddSessionDialog
from WorkersWidget.SessionsWidget.ChangeSessionDialog import ChangeSessionDialog
from sqlalchemy import select, func, insert, update, delete
from Models.Film import Film
from Models.Hall import Hall
from Models.Cinema import Cinema
from Models.City import City
from Models.Shedule import Shedule
from Models.TypeOfHall import TypeOfHall
from Models.Seat import Seat
from Models.Session import Session

class SessionsWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(SessionsWidget, self).__init__(*args, **kwargs)
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
        self.listOfSessions = QtWidgets.QTableWidget()
        self.listOfSessions.setEditTriggers(self.listOfSessions.EditTrigger.NoEditTriggers)
        self.listOfSessions.setSelectionMode(self.listOfSessions.SelectionMode.SingleSelection)
        self.listOfSessions.setSelectionBehavior(self.listOfSessions.SelectionBehavior.SelectRows)
        self.listOfSessions.setColumnCount(5)
        self.listOfSessions.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem('Фильм'))
        self.listOfSessions.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem('Дата'))
        self.listOfSessions.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem('Время'))
        self.listOfSessions.setHorizontalHeaderItem(3, QtWidgets.QTableWidgetItem('Зал'))
        self.listOfSessions.setHorizontalHeaderItem(4, QtWidgets.QTableWidgetItem('Цена'))
        self.listOfSessions.pressed.connect(self.changeEnableButtons)
        self.vBoxLayout.addWidget(self.listOfSessions)
        self.vBoxLayout.addWidget(self.widgetWithButtons)
        self.setLayout(self.vBoxLayout)
        self.updateData()

    def updateData(self):
        self.listOfSessions.setRowCount(0)
        with engine.connect() as conn:
            index = 0
            query = (select(Session.id, Session.dateTimeStart, Session.priceFilm, Session.idShedule,
                            Shedule.idFilm, Shedule.idHall, Film.name, Hall.number, City.name, Cinema.street)
                     .join(Shedule, Shedule.id == Session.idShedule)
                     .join(Film, Film.id == Shedule.idFilm)
                     .join(Hall, Hall.id == Shedule.idHall)
                     .join(Cinema, Cinema.id == Hall.idCinema)
                     .join(City, City.id == Cinema.idCity)
                     .order_by(Shedule.date, Film.name, City.name, Cinema.street, Hall.number))
            for row in conn.execute(query):
                item = QtWidgets.QTableWidgetItem(row[6])
                item.setData(1, row[0])
                self.listOfSessions.insertRow(index)
                self.listOfSessions.setItem(index, 0, item)
                item1 = QtWidgets.QTableWidgetItem(str(row[1].day) + '.' + str(row[1].month) + '.' + str(row[1].year))
                item1.setData(1, row[3])
                self.listOfSessions.setItem(index, 1, item1)
                item2 = QtWidgets.QTableWidgetItem(str(row[1].hour) + ':' + str(row[1].minute))
                self.listOfSessions.setItem(index, 2, item2)
                item3 = QtWidgets.QTableWidgetItem(row[8] + ', ' + row[9] + ', ' + row[7])
                self.listOfSessions.setItem(index, 3, item3)
                item4 = QtWidgets.QTableWidgetItem(str(row[2]))
                self.listOfSessions.setItem(index, 4, item4)
                index += 1
            self.addButton.setEnabled(False)\
                if len(conn.execute(select(Shedule)).all()) == 0 else self.addButton.setEnabled(True)
            conn.close()
        self.changeEnableButtons()

    def addButtonClicked(self):
        query = (select(Shedule.id, Shedule.date, Film.name, City.name, Cinema.street, Hall.number)
                 .join(Film, Film.id == Shedule.idFilm)
                 .join(Hall, Hall.id == Shedule.idHall)
                 .join(Cinema, Cinema.id == Hall.idCinema)
                 .join(City, City.id == City.id)
                 .order_by(Shedule.date, Film.name, City.name, Cinema.street, Hall.number))
        listOfShedule = []
        with engine.connect() as conn:
            for row in conn.execute(query):
                listOfShedule.append((row[0], str(row[1].day) + '.' + str(row[1].month) + '.' + str(row[1].year)
                                       + ' ' + row[2] + ' ' + row[3] + ', ' + row[4] + ', ' + row[5], row[1]))
            conn.close()
        self.addSessionDialog = AddSessionDialog(listOfShedule)
        while True:
            self.addSessionDialog.listOfShedule.setEnabled(True)
            self.addSessionDialog.exec()
            if self.addSessionDialog.listOfShedule.isEnabled():
                break
            else:
                with engine.connect() as conn:
                    dateShedule = conn.execute(select(Shedule.date).where(Shedule.id == self.addSessionDialog.listOfShedule
                                                            .itemData(self.addSessionDialog.listOfShedule
                                                                      .currentIndex(), 1))).all()[0][0]
                    conn.execute(
                        insert(Session),
                        [
                            {'priceFilm': self.addSessionDialog.price.value(),
                             'dateTimeStart': str(dateShedule.day) + '-' + str(dateShedule.month)
                                              + '-' + str(dateShedule.year)
                                              + ' ' + self.addSessionDialog.time.time().toString('H:mm'),
                             'idShedule': self.addSessionDialog.listOfShedule.itemData(
                                 self.addSessionDialog.listOfShedule.currentIndex(), 1)},
                        ]
                    )
                    shedule = conn.execute(select(Shedule.idHall).where(Shedule.id == self.addSessionDialog.listOfShedule.itemData(
                                 self.addSessionDialog.listOfShedule.currentIndex(), 1))).all()[0]
                    hall = conn.execute(select(Hall.idTypeOfHall).where(Hall.id == shedule[0])).all()[0]
                    typeOfHall = conn.execute(select(TypeOfHall).where(TypeOfHall.id == hall[0])).all()[0]
                    countOfRows = typeOfHall[2]
                    countOfColums = typeOfHall[3]
                    sessions = conn.execute(select(Session)).all()
                    session = sessions[len(sessions) - 1]
                    for i in range(countOfRows):
                        for j in range(countOfColums):
                            conn.execute(
                                insert(Seat),
                                [
                                    {
                                        'numberRow': i,
                                        'numberCol': j,
                                        'idSession': session[0]
                                    }
                                ]
                            )
                    conn.close()
                    self.updateData()
                    break

    def changeButtonClicked(self):
        if len(self.listOfSessions.selectedItems()) == 5:
            query = (select(Shedule.id, Shedule.date, Film.name, City.name, Cinema.street, Hall.number)
                     .join(Film, Film.id == Shedule.idFilm)
                     .join(Hall, Hall.id == Shedule.idHall)
                     .join(Cinema, Cinema.id == Hall.idCinema)
                     .join(City, City.id == City.id)
                     .order_by(Shedule.date, Film.name, City.name, Cinema.street, Hall.number))
            listOfShedule = []
            with engine.connect() as conn:
                for row in conn.execute(query):
                    listOfShedule.append((row[0], str(row[1].day) + '.' + str(row[1].month) + '.' + str(row[1].year)
                                          + ' ' + row[2] + ' ' + row[3] + ', ' + row[4] + ', ' + row[5], row[1]))
                conn.close()
                previousTimeItem = self.listOfSessions.item(self.listOfSessions.currentRow(), 2).text().split(':')
                previousTime = time(int(previousTimeItem[0]), int(previousTimeItem[1]), 0)
            self.changeSessionDialog = ChangeSessionDialog(
                listOfShedule,
                previousTime,
                float(self.listOfSessions.item(self.listOfSessions.currentRow(), 4).text()),
                self.listOfSessions.item(self.listOfSessions.currentRow(), 1).data(1))
            while True:
                self.changeSessionDialog.listOfShedule.setEnabled(True)
                self.changeSessionDialog.exec()
                if self.changeSessionDialog.listOfShedule.isEnabled():
                    break
                else:
                    with engine.connect() as conn:
                        dateShedule = \
                        conn.execute(select(Shedule.date).where(Shedule.id == self.changeSessionDialog.listOfShedule
                                                                .itemData(self.changeSessionDialog.listOfShedule
                                                                          .currentIndex(), 1))).all()[0][0]
                        conn.execute(
                            update(Session)
                                .values(id=self.listOfSessions.item(self.listOfSessions.currentRow(), 0).data(1),
                                        priceFilm=self.changeSessionDialog.price.value(),
                                        dateTimeStart=str(dateShedule.day) + '-' + str(dateShedule.month)
                                                      + '-' + str(dateShedule.year)
                                                      + ' ' + self.changeSessionDialog.time.time().toString('H:mm'),
                                 idShedule=self.changeSessionDialog.listOfShedule.itemData(
                                     self.changeSessionDialog.listOfShedule.currentIndex(), 1))
                        )
                        conn.close()
                        self.updateData()
                        break

    def deleteButtonClicked(self):
        if self.listOfSessions.currentRow() > -1:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setWindowTitle('Удаление расписания')
            messageBox.addButton('Удалить', 5)
            messageBox.addButton('Отменить', 6)
            messageBox.setText('Удалить сеанс?')
            reply = messageBox.exec()
            if reply == 0:
                with engine.connect() as conn:
                    query = (select(func.count())
                             .where(Session.id ==
                                    self.listOfSessions.item(self.listOfSessions.currentRow(), 0).data(1)))
                    if conn.execute(query).all()[0][0] != 1:
                        messageBox = QtWidgets.QMessageBox()
                        messageBox.setWindowTitle('Ошибка')
                        messageBox.addButton('Ок', 5)
                        messageBox.setText('Сеанса не существует!')
                        messageBox.exec()
                        conn.close()
                    else:
                        conn.execute(
                            delete(Session)
                                .where(Session.id == self.listOfSessions.item
                            (self.listOfSessions.currentRow(), 0).data(1))
                        )
                        conn.close()
                        self.updateData()

    def changeEnableButtons(self):
        if len(self.listOfSessions.selectedItems()) != 5:
            self.changeButton.setEnabled(False)
            self.deleteButton.setEnabled(False)
        else:
            self.changeButton.setEnabled(True)
            self.deleteButton.setEnabled(True)