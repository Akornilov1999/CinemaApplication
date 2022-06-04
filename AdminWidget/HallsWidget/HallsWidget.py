from PyQt5 import QtWidgets
from declaration import engine
from AdminWidget.HallsWidget.AddHallDIalog import AddHallDialog
from AdminWidget.HallsWidget.ChangeHallDialog import ChangeHallDialog
from sqlalchemy import select, func, insert, update, delete
from Models.Hall import Hall
from Models.Seat import Seat
from Models.Cinema import Cinema
from Models.City import City
from Models.TypeOfHall import TypeOfHall

class HallsWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(HallsWidget, self).__init__(*args, **kwargs)
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
        self.listOfHalls = QtWidgets.QTableWidget()
        self.listOfHalls.setEditTriggers(self.listOfHalls.EditTrigger.NoEditTriggers)
        self.listOfHalls.setSelectionMode(self.listOfHalls.SelectionMode.SingleSelection)
        self.listOfHalls.setSelectionBehavior(self.listOfHalls.SelectionBehavior.SelectRows)
        self.listOfHalls.setColumnCount(4)
        self.listOfHalls.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem('Номер'))
        self.listOfHalls.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem('Улица'))
        self.listOfHalls.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem('Город'))
        self.listOfHalls.setHorizontalHeaderItem(3, QtWidgets.QTableWidgetItem('Тип зала'))
        self.listOfHalls.pressed.connect(self.changeEnableButtons)
        self.vBoxLayout.addWidget(self.listOfHalls)
        self.vBoxLayout.addWidget(self.widgetWithButtons)
        self.setLayout(self.vBoxLayout)
        self.updateData()

    def updateData(self):
        self.listOfHalls.setRowCount(0)
        with engine.connect() as conn:
            index = 0
            query = (select(Hall.id, Hall.number, Cinema.street,
                            City.id, City.name, TypeOfHall.id, TypeOfHall.type)
                     .join(Cinema, Cinema.id == Hall.idCinema)
                     .join(City, City.id == Cinema.idCity)
                     .join(TypeOfHall, TypeOfHall.id == Hall.idTypeOfHall)
                     .order_by(Hall.number, Cinema.street, City.name, TypeOfHall.type))
            for row in conn.execute(query):
                item = QtWidgets.QTableWidgetItem(row[1])
                item.setData(1, row[0])
                self.listOfHalls.insertRow(index)
                self.listOfHalls.setItem(index, 0, item)
                item1 = QtWidgets.QTableWidgetItem(str(row[3]))
                item1.setData(1, row[2])
                self.listOfHalls.setItem(index, 1, item1)
                item2 = QtWidgets.QTableWidgetItem(str(row[4]))
                self.listOfHalls.setItem(index, 2, item2)
                item3 = QtWidgets.QTableWidgetItem(str(row[6]))
                item3.setData(1, row[5])
                self.listOfHalls.setItem(index, 3, item3)
                index += 1
        self.changeEnableButtons()

    def addButtonClicked(self):
        query = (select(Cinema.id, Cinema.street, City.name).
                 join(City, City.id == Cinema.idCity).order_by(Cinema.street, City.name))
        query1 = (select(TypeOfHall.id, TypeOfHall.type).order_by(TypeOfHall.type))
        listOfCinemas = []
        with engine.connect() as conn:
            for row in conn.execute(query):
                listOfCinemas.append((row[0], row[1] + ', ' +row[2]))
            conn.close()
        listOfTypesOfHall = []
        with engine.connect() as conn:
            for row in conn.execute(query1):
                listOfTypesOfHall.append((row[0], row[1]))
            conn.close()
        self.addHallDialog = AddHallDialog(listOfCinemas, listOfTypesOfHall)
        while True:
            self.addHallDialog.lineEdit.setEnabled(True)
            self.addHallDialog.exec()
            if self.addHallDialog.lineEdit.isEnabled():
                break
            elif not self.addHallDialog.lineEdit.isEnabled() and self.addHallDialog.lineEdit.text() == '':
                messageBox = QtWidgets.QMessageBox()
                messageBox.setWindowTitle('Ошибка')
                messageBox.addButton('Ок', 5)
                messageBox.setText('Не был введен номер!')
                messageBox.exec()
            else:
                query = (select(func.count()).
                                where(Cinema.id == self.addHallDialog.listOfCinemas.itemData(
                    self.addHallDialog.listOfCinemas.currentIndex(), 1)))
                query1 = (select(func.count()).
                         where(TypeOfHall.id == self.addHallDialog.listOfTypesOfHall.itemData(
                    self.addHallDialog.listOfTypesOfHall.currentIndex(), 1)))
                with engine.connect() as conn:
                    if conn.execute(query).all()[0][0] != 1:
                        messageBox = QtWidgets.QMessageBox()
                        messageBox.setWindowTitle('Ошибка')
                        messageBox.addButton('Ок', 5)
                        messageBox.setText('Выбранного кинотеатра не существует!')
                        messageBox.exec()
                        conn.close()
                    elif conn.execute(query1).all()[0][0] != 1:
                            messageBox = QtWidgets.QMessageBox()
                            messageBox.setWindowTitle('Ошибка')
                            messageBox.addButton('Ок', 5)
                            messageBox.setText('Выбранного типа зала не существует!')
                            messageBox.exec()
                            conn.close()
                    else:
                        conn.execute(
                            insert(Hall),
                            [
                                {'number': self.addHallDialog.lineEdit.text(),
                                 'idCinema': self.addHallDialog.listOfCinemas.itemData(
                                     self.addHallDialog.listOfCinemas.currentIndex(), 1),
                                 'idTypeOfHall': self.addHallDialog.listOfTypesOfHall.itemData(
                                     self.addHallDialog.listOfTypesOfHall.currentIndex(), 1)},
                            ]
                        )
                        '''query2 = (select(TypeOfHall).where(TypeOfHall.id
                                                           == self.addHallDialog.listOfTypesOfHall.itemData(
                                     self.addHallDialog.listOfTypesOfHall.currentIndex(), 1)))
                        query3 = (select(Hall))
                        countOfRows = conn.execute(query2).all()[0][2]
                        countOfColums = conn.execute(query2).all()[0][3]
                        idHall = conn.execute(query3).all()[len(conn.execute(query3).all()) - 1][0]
                        for i in range(countOfRows):
                            for j in range(countOfColums):
                                conn.execute(
                                    insert(Seat),
                                    [
                                        {
                                            'numberRow': i,
                                            'numberCol': j,
                                            'idHall':  idHall
                                        }
                                    ]
                                )'''
                        conn.close()
                        self.updateData()
                        break

    def changeButtonClicked(self):
        if len(self.listOfHalls.selectedItems()) == 4:
            query = (select(Cinema.id, Cinema.street, City.name).
                     join(City, City.id == Cinema.idCity).order_by(Cinema.street, City.name))
            query1 = (select(TypeOfHall.id, TypeOfHall.type).order_by(TypeOfHall.type))
            listOfCinemas = []
            with engine.connect() as conn:
                for row in conn.execute(query):
                    listOfCinemas.append((row[0], row[1] + ', ' + row[2]))
                conn.close()
            listOfTypesOfHall = []
            with engine.connect() as conn:
                for row in conn.execute(query1):
                    listOfTypesOfHall.append((row[0], row[1]))
                conn.close()
            self.changeHallDialog = ChangeHallDialog(
                listOfCinemas, listOfTypesOfHall,
                self.listOfHalls.item(self.listOfHalls.currentRow(), 0).text(),
                self.listOfHalls.item(self.listOfHalls.currentRow(), 1).data(1),
                self.listOfHalls.item(self.listOfHalls.currentRow(), 3).data(1))
            while True:
                self.changeHallDialog.lineEdit.setEnabled(True)
                self.changeHallDialog.exec()
                if self.changeHallDialog.lineEdit.isEnabled():
                    break
                elif not self.changeHallDialog.lineEdit.isEnabled() \
                        and self.changeHallDialog.lineEdit.text() == '':
                    messageBox = QtWidgets.QMessageBox()
                    messageBox.setWindowTitle('Ошибка')
                    messageBox.addButton('Ок', 5)
                    messageBox.setText('Не был введен номер!')
                    messageBox.exec()
                else:
                    with engine.connect() as conn:
                            conn.execute(
                                update(Hall)
                                    .values(number=self.changeHallDialog.lineEdit.text(),
                                            idCinema=self.changeHallDialog.listOfCinemas.itemData(
                                                self.changeHallDialog.listOfCinemas.currentIndex(), 1),
                                            idTypeOfHall=self.changeHallDialog.listOfTypesOfHall.itemData(
                                                self.changeHallDialog.listOfTypesOfHall.currentIndex(), 1))
                                    .where(Hall.id == self.listOfHalls.item(self.listOfHalls.currentRow(), 0).data(1))
                            )
                            '''conn.execute(
                                delete(Seat).where(Seat.idHall
                                                   == self.listOfHalls.item(self.listOfHalls.currentRow(), 0).data(1))
                            )
                            query2 = (select(TypeOfHall).where(TypeOfHall.id
                                                               == self.addHallDialog.listOfTypesOfHall.itemData(
                                self.addHallDialog.listOfTypesOfHall.currentIndex(), 1)))
                            countOfRows = conn.execute(query2).all()[0][2]
                            countOfColums = conn.execute(query2).all()[0][3]
                            for i in range(countOfRows):
                                for j in range(countOfColums):
                                    conn.execute(
                                        insert(Seat),
                                        [
                                            {
                                                'numberRow': i,
                                                'numberCol': j,
                                                'idHall': self.listOfHalls
                                                    .item(self.listOfHalls.currentRow(), 0).data(1)
                                            }
                                        ]
                                    )'''
                            conn.close()
                            self.updateData()
                            break

    def deleteButtonClicked(self):
        if self.listOfHalls.currentRow() > -1:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setWindowTitle('Удаление зала')
            messageBox.addButton('Удалить', 5)
            messageBox.addButton('Отменить', 6)
            messageBox.setText('Удалить зал \"'
                               + self.listOfHalls.item(self.listOfHalls.currentRow(), 0).text() + '\"?')
            reply = messageBox.exec()
            if reply == 0:
                with engine.connect() as conn:
                    query = (select(func.count())
                             .where(Hall.id ==
                                    self.listOfHalls.item(self.listOfHalls.currentRow(), 0).data(1)))
                    if conn.execute(query).all()[0][0] != 1:
                        messageBox = QtWidgets.QMessageBox()
                        messageBox.setWindowTitle('Ошибка')
                        messageBox.addButton('Ок', 5)
                        messageBox.setText('Зал с номером \"'
                                           + self.listOfHalls.item(self.listOfHalls.currentRow(), 0).text()
                                           + '\" не существует!')
                        messageBox.exec()
                        conn.close()
                    else:
                        conn.execute(
                            delete(Hall)
                                .where(Hall.id == self.listOfHalls.item(self.listOfHalls.currentRow(), 0).data(1))
                        )
                        conn.close()
                        self.updateData()

    def changeEnableButtons(self):
        if len(self.listOfHalls.selectedItems()) != 4:
            self.changeButton.setEnabled(False)
            self.deleteButton.setEnabled(False)
        else:
            self.changeButton.setEnabled(True)
            self.deleteButton.setEnabled(True)