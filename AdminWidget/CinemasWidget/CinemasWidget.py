from PyQt5 import QtWidgets
from declaration import engine
from AdminWidget.CinemasWidget.AddCinemaDialog import AddCinemaDialog
from AdminWidget.CinemasWidget.ChangeCinemaDialog import ChangeCinemaDialog
from sqlalchemy import select, func, insert, update, delete
from Models.City import City
from Models.Cinema import Cinema

class CinemasWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(CinemasWidget, self).__init__(*args, **kwargs)
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
        self.listOfCinemas = QtWidgets.QTableWidget()
        self.listOfCinemas.setEditTriggers(self.listOfCinemas.EditTrigger.NoEditTriggers)
        self.listOfCinemas.setSelectionMode(self.listOfCinemas.SelectionMode.SingleSelection)
        self.listOfCinemas.setSelectionBehavior(self.listOfCinemas.SelectionBehavior.SelectRows)
        self.listOfCinemas.setColumnCount(2)
        self.listOfCinemas.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem('Улица'))
        self.listOfCinemas.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem('Город'))
        self.listOfCinemas.pressed.connect(self.changeEnableButtons)
        self.vBoxLayout.addWidget(self.listOfCinemas)
        self.vBoxLayout.addWidget(self.widgetWithButtons)
        self.setLayout(self.vBoxLayout)
        self.updateData()

    def updateData(self):
        self.listOfCinemas.setRowCount(0)
        with engine.connect() as conn:
            index = 0
            query = (select(Cinema, City).join(City, City.id == Cinema.idCity).order_by(Cinema.street, City.name))
            for row in conn.execute(query):
                item = QtWidgets.QTableWidgetItem(row[1])
                item.setData(1, row[0])
                self.listOfCinemas.insertRow(index)
                self.listOfCinemas.setItem(index, 0, item)
                item1 = QtWidgets.QTableWidgetItem(str(row[4]))
                item1.setData(1, row[2])
                self.listOfCinemas.setItem(index, 1, item1)
                index += 1
        self.changeEnableButtons()

    def addButtonClicked(self):
        query = (select(City).order_by(City.name))
        listOfCities = []
        with engine.connect() as conn:
            for row in conn.execute(query):
                listOfCities.append((row[0], row[1]))
            conn.close()
        self.addCinemaDialog = AddCinemaDialog(listOfCities)
        while True:
            self.addCinemaDialog.lineEdit.setEnabled(True)
            self.addCinemaDialog.exec()
            if self.addCinemaDialog.lineEdit.isEnabled():
                break
            elif not self.addCinemaDialog.lineEdit.isEnabled() and self.addCinemaDialog.lineEdit.text() == '':
                messageBox = QtWidgets.QMessageBox()
                messageBox.setWindowTitle('Ошибка')
                messageBox.addButton('Ок', 5)
                messageBox.setText('Не была введена улица!')
                messageBox.exec()
            else:
                query = (select(func.count()).
                                where(City.id == self.addCinemaDialog.listOfCities.itemData(
                    self.addCinemaDialog.listOfCities.currentIndex(), 1)))
                with engine.connect() as conn:
                    if conn.execute(query).all()[0][0] != 1:
                        messageBox = QtWidgets.QMessageBox()
                        messageBox.setWindowTitle('Ошибка')
                        messageBox.addButton('Ок', 5)
                        messageBox.setText('Выбранного города не существует!')
                        messageBox.exec()
                        conn.close()
                    else:
                        conn.execute(
                            insert(Cinema),
                            [
                                {'street': self.addCinemaDialog.lineEdit.text(),
                                 'idCity': self.addCinemaDialog.listOfCities.itemData(
                                     self.addCinemaDialog.listOfCities.currentIndex(), 1)},
                            ]
                        )
                        conn.close()
                        self.updateData()
                        break

    def changeButtonClicked(self):
        if len(self.listOfCinemas.selectedItems()) == 2:
            query = (select(City).order_by(City.name))
            listOfCities = []
            with engine.connect() as conn:
                for row in conn.execute(query):
                    listOfCities.append((row[0], row[1]))
                conn.close()
            self.changeCityDialog = ChangeCinemaDialog(
                listOfCities,
                self.listOfCinemas.item(self.listOfCinemas.currentRow(), 0).text(),
                self.listOfCinemas.item(self.listOfCinemas.currentRow(), 1).data(1))
            while True:
                self.changeCityDialog.lineEdit.setEnabled(True)
                self.changeCityDialog.exec()
                if self.changeCityDialog.lineEdit.isEnabled():
                    break
                elif not self.changeCityDialog.lineEdit.isEnabled() \
                        and self.changeCityDialog.lineEdit.text() == '':
                    messageBox = QtWidgets.QMessageBox()
                    messageBox.setWindowTitle('Ошибка')
                    messageBox.addButton('Ок', 5)
                    messageBox.setText('Не была введена улица!')
                    messageBox.exec()
                else:
                    with engine.connect() as conn:
                            conn.execute(
                                update(Cinema).values(street=self.changeCityDialog.lineEdit.text(),
                                                      idCity=self.changeCityDialog.listOfCities.itemData(
                                                          self.changeCityDialog.listOfCities.currentIndex(), 1)).
                                    where(Cinema.id ==
                                          self.listOfCinemas.item(self.listOfCinemas.currentRow(), 0).data(1))
                            )
                            conn.close()
                            self.updateData()
                            break


    def deleteButtonClicked(self):
        if self.listOfCinemas.currentRow() > -1:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setWindowTitle('Удаление кинотеатра')
            messageBox.addButton('Удалить', 5)
            messageBox.addButton('Отменить', 6)
            messageBox.setText('Удалить кинотеатр по адресу \"' +
                               self.listOfCinemas.item(self.listOfCinemas.currentRow(), 1).text() + ', ' +
                               self.listOfCinemas.item(self.listOfCinemas.currentRow(), 0).text() + '\"?')
            reply = messageBox.exec()
            if reply == 0:
                with engine.connect() as conn:
                    query = (select(func.count()).
                              where(Cinema.id ==
                                    self.listOfCinemas.item(self.listOfCinemas.currentRow(), 0).data(1)))
                    if conn.execute(query).all()[0][0] != 1:
                        messageBox = QtWidgets.QMessageBox()
                        messageBox.setWindowTitle('Ошибка')
                        messageBox.addButton('Ок', 5)
                        messageBox.setText('Кинотеатр по адресу \"' +
                               self.listOfCinemas.item(self.listOfCinemas.currentRow(), 1).text() + ', ' +
                               self.listOfCinemas.item(self.listOfCinemas.currentRow(), 0).text() + '\" не существует!')
                        messageBox.exec()
                        conn.close()
                    else:
                        conn.execute(
                            delete(Cinema).
                                where(Cinema.id ==
                                      self.listOfCinemas.item(self.listOfCinemas.currentRow(), 0).data(1))
                        )
                        conn.close()
                        self.updateData()

    def changeEnableButtons(self):
        if len(self.listOfCinemas.selectedItems()) != 2:
            self.changeButton.setEnabled(False)
            self.deleteButton.setEnabled(False)
        else:
            self.changeButton.setEnabled(True)
            self.deleteButton.setEnabled(True)