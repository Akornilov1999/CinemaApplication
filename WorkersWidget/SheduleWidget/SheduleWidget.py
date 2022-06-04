from PyQt5 import QtWidgets
from datetime import date
from declaration import engine
from WorkersWidget.SheduleWidget.AddSheduleDialog import AddSheduleDialog
from WorkersWidget.SheduleWidget.ChangeSheduleDialog import ChangeSheduleDialog
from sqlalchemy import select, func, insert, update, delete
from Models.Film import Film
from Models.Hall import Hall
from Models.Cinema import Cinema
from Models.City import City
from Models.Shedule import Shedule

class SheduleWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(SheduleWidget, self).__init__(*args, **kwargs)
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
        self.listOfShedule = QtWidgets.QTableWidget()
        self.listOfShedule.setEditTriggers(self.listOfShedule.EditTrigger.NoEditTriggers)
        self.listOfShedule.setSelectionMode(self.listOfShedule.SelectionMode.SingleSelection)
        self.listOfShedule.setSelectionBehavior(self.listOfShedule.SelectionBehavior.SelectRows)
        self.listOfShedule.setColumnCount(3)
        self.listOfShedule.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem('Дата'))
        self.listOfShedule.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem('Фильм'))
        self.listOfShedule.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem('Зал'))
        self.listOfShedule.pressed.connect(self.changeEnableButtons)
        self.vBoxLayout.addWidget(self.listOfShedule)
        self.vBoxLayout.addWidget(self.widgetWithButtons)
        self.setLayout(self.vBoxLayout)
        self.updateData()

    def updateData(self):
        self.listOfShedule.setRowCount(0)
        with engine.connect() as conn:
            index = 0
            query = (select(Shedule.id, Shedule.date, Shedule.idFilm, Shedule.idHall, Film.name, Hall.number,
                            City.name, Cinema.street)
                     .join(Film, Film.id == Shedule.idFilm)
                     .join(Hall, Hall.id == Shedule.idHall)
                     .join(Cinema, Cinema.id == Hall.idCinema)
                     .join(City, City.id == Cinema.idCity)
                     .order_by(Shedule.date, Film.name, City.name, Cinema.street, Hall.number))
            for row in conn.execute(query):
                item = QtWidgets.QTableWidgetItem(str(row[1].day) + '.' + str(row[1].month) + '.' + str(row[1].year))
                item.setData(1, row[0])
                self.listOfShedule.insertRow(index)
                self.listOfShedule.setItem(index, 0, item)
                item1 = QtWidgets.QTableWidgetItem(row[4])
                item1.setData(1, row[2])
                self.listOfShedule.setItem(index, 1, item1)
                item2 = QtWidgets.QTableWidgetItem(row[6] + ', ' + row[7] + ', ' + row[5])
                item2.setData(1, row[3])
                self.listOfShedule.setItem(index, 2, item2)
                index += 1
            self.addButton.setEnabled(False)\
                if len(conn.execute(select(Film)).all()) == 0 or len(conn.execute(select(Hall)).all()) == 0\
                else self.addButton.setEnabled(True)
            conn.close()
        self.changeEnableButtons()

    def addButtonClicked(self):
        query = (select(Film.id, Film.name).order_by(Film.name))
        query1 = (select(Hall.id, City.name, Cinema.street, Hall.number)
                  .join(Cinema, Cinema.id == Hall.idCinema)
                  .join(City, City.id == Cinema.idCity)
                  .order_by(City.name, Cinema.street, Hall.number))
        listOfFilms = []
        with engine.connect() as conn:
            for row in conn.execute(query):
                listOfFilms.append((row[0], row[1]))
            conn.close()
        listOfHalls = []
        with engine.connect() as conn:
            for row in conn.execute(query1):
                listOfHalls.append((row[0], row[1] + ', ' + row[2] + ', ' + row[3]))
            conn.close()
        self.addSheduleDialog = AddSheduleDialog(listOfFilms, listOfHalls)
        while True:
            self.addSheduleDialog.listOfFilms.setEnabled(True)
            self.addSheduleDialog.exec()
            if self.addSheduleDialog.listOfFilms.isEnabled():
                break
            else:
                query = (select(func.count())
                         .where(Shedule.date == self.addSheduleDialog.date.selectedDate().toString('dd-MM-yyyy'))
                         .where(Shedule.idHall == self.addSheduleDialog.listOfHalls.itemData
                (self.addSheduleDialog.listOfHalls.currentIndex(), 1)))
                with engine.connect() as conn:
                    if conn.execute(query).all()[0][0] > 0:
                        messageBox = QtWidgets.QMessageBox()
                        messageBox.setWindowTitle('Ошибка')
                        messageBox.addButton('Ок', 5)
                        messageBox.setText('Такое расписание уже существует!')
                        messageBox.exec()
                        conn.close()
                    else:
                        conn.execute(
                            insert(Shedule),
                            [
                                {'date': self.addSheduleDialog.date.selectedDate().toString('dd-MM-yyyy'),
                                'idFilm': self.addSheduleDialog.listOfFilms.itemData(
                                     self.addSheduleDialog.listOfFilms.currentIndex(), 1),
                                 'idHall': self.addSheduleDialog.listOfHalls.itemData(
                                     self.addSheduleDialog.listOfHalls.currentIndex(), 1)},
                            ]
                        )
                        conn.close()
                        self.updateData()
                        break

    def changeButtonClicked(self):
        if len(self.listOfShedule.selectedItems()) == 3:
            query = (select(Film.id, Film.name).order_by(Film.name))
            query1 = (select(Hall.id, City.name, Cinema.street, Hall.number)
                      .join(Cinema, Cinema.id == Hall.idCinema)
                      .join(City, City.id == Cinema.idCity)
                      .order_by(City.name, Cinema.street, Hall.number))
            listOfFilms = []
            with engine.connect() as conn:
                for row in conn.execute(query):
                    listOfFilms.append((row[0], row[1]))
                conn.close()
            listOfHalls = []
            with engine.connect() as conn:
                for row in conn.execute(query1):
                    listOfHalls.append((row[0], row[1] + ', ' + row[2] + ', ' + row[3]))
                conn.close()
                previousDate = self.listOfShedule.item(self.listOfShedule.currentRow(), 0).text().split('.')
            self.changeSheduleDialog = ChangeSheduleDialog(
                listOfFilms, listOfHalls,
                date(int(previousDate[2]), int(previousDate[1]), int(previousDate[0])),
                self.listOfShedule.item(self.listOfShedule.currentRow(), 1).data(1),
                self.listOfShedule.item(self.listOfShedule.currentRow(), 2).data(1))
            while True:
                self.changeSheduleDialog.listOfFilms.setEnabled(True)
                self.changeSheduleDialog.exec()
                if self.changeSheduleDialog.listOfFilms.isEnabled():
                    break
                else:
                    with engine.connect() as conn:
                        if conn.execute(select(func.count())
                         .where(Shedule.date == self.changeSheduleDialog.date.selectedDate().toString('dd-MM-yyyy'))
                         .where(Shedule.idHall == self.changeSheduleDialog.listOfHalls.itemData
                (self.changeSheduleDialog.listOfHalls.currentIndex(), 1))
                                                    .where(Shedule.id != self.listOfShedule
                                .item(self.listOfShedule.currentRow(), 0).data(1))).all()[0][0] > 0:
                            messageBox = QtWidgets.QMessageBox()
                            messageBox.setWindowTitle('Ошибка')
                            messageBox.addButton('Ок', 5)
                            messageBox.setText('Такое расписание уже существует!')
                            messageBox.exec()
                            conn.close()
                        else:
                            conn.execute(
                                update(Shedule)
                                    .values(idFilm=self.changeSheduleDialog.listOfFilms.itemData(
                                                self.changeSheduleDialog.listOfFilms.currentIndex(), 1),
                                            idHall=self.changeSheduleDialog.listOfHalls.itemData(
                                                self.changeSheduleDialog.listOfHalls.currentIndex(), 1))
                                    .where(Shedule.id == self.listOfShedule.item
                                (self.listOfShedule.currentRow(), 0).data(1))
                            )
                            conn.close()
                            self.updateData()
                            break

    def deleteButtonClicked(self):
        if self.listOfShedule.currentRow() > -1:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setWindowTitle('Удаление расписания')
            messageBox.addButton('Удалить', 5)
            messageBox.addButton('Отменить', 6)
            messageBox.setText('Удалить расписание?')
            reply = messageBox.exec()
            if reply == 0:
                with engine.connect() as conn:
                    query = (select(func.count())
                             .where(Shedule.id ==
                                    self.listOfShedule.item(self.listOfShedule.currentRow(), 0).data(1)))
                    if conn.execute(query).all()[0][0] != 1:
                        messageBox = QtWidgets.QMessageBox()
                        messageBox.setWindowTitle('Ошибка')
                        messageBox.addButton('Ок', 5)
                        messageBox.setText('Расписания не существует!')
                        messageBox.exec()
                        conn.close()
                    else:
                        conn.execute(
                            delete(Shedule)
                                .where(Shedule.id == self.listOfShedule.item
                            (self.listOfShedule.currentRow(), 0).data(1))
                        )
                        conn.close()
                        self.updateData()

    def changeEnableButtons(self):
        if len(self.listOfShedule.selectedItems()) != 3:
            self.changeButton.setEnabled(False)
            self.deleteButton.setEnabled(False)
        else:
            self.changeButton.setEnabled(True)
            self.deleteButton.setEnabled(True)