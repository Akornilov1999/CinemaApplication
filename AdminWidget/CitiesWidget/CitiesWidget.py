from PyQt5 import QtWidgets
from declaration import engine
from AdminWidget.CitiesWidget.AddCityDialog import AddCityDialog
from AdminWidget.CitiesWidget.RenameCityDialog import RenameCityDialog
from sqlalchemy import select, func, insert, update, delete
from Models.City import City

class CitiesWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(CitiesWidget, self).__init__(*args, **kwargs)
        self.addButton = QtWidgets.QPushButton('Добавить')
        self.addButton.clicked.connect(self.addButtonClicked)
        self.renameButton = QtWidgets.QPushButton('Переименовать')
        self.renameButton.clicked.connect(self.renameButtonClicked)
        self.deleteButton = QtWidgets.QPushButton('Удалить')
        self.deleteButton.clicked.connect(self.deleteButtonClicked)
        self.hBoxLayout = QtWidgets.QHBoxLayout()
        self.hBoxLayout.addWidget(self.addButton)
        self.hBoxLayout.addWidget(self.renameButton)
        self.hBoxLayout.addWidget(self.deleteButton)
        self.widgetWithButtons = QtWidgets.QWidget()
        self.widgetWithButtons.setLayout(self.hBoxLayout)
        self.vBoxLayout = QtWidgets.QVBoxLayout()
        self.listOfCities = QtWidgets.QTableWidget()
        self.listOfCities.setEditTriggers(self.listOfCities.EditTrigger.NoEditTriggers)
        self.listOfCities.setSelectionMode(self.listOfCities.SelectionMode.SingleSelection)
        self.listOfCities.setSelectionBehavior(self.listOfCities.SelectionBehavior.SelectRows)
        self.listOfCities.setColumnCount(1)
        self.listOfCities.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem('Наименование'))
        self.listOfCities.pressed.connect(self.changeEnableButtons)
        self.vBoxLayout.addWidget(self.listOfCities)
        self.vBoxLayout.addWidget(self.widgetWithButtons)
        self.setLayout(self.vBoxLayout)
        self.updateData()

    def updateData(self):
        self.listOfCities.setRowCount(0)
        with engine.connect() as conn:
            index = 0
            query = (select(City).order_by(City.name))
            for row in conn.execute(query):
                item = QtWidgets.QTableWidgetItem(row[1])
                item.setData(1, row[0])
                self.listOfCities.insertRow(index)
                self.listOfCities.setItem(index, 0, item)
                index += 1
        self.changeEnableButtons()

    def addButtonClicked(self):
        self.addCityDialog = AddCityDialog()
        while True:
            self.addCityDialog.lineEdit.setEnabled(True)
            self.addCityDialog.exec()
            if self.addCityDialog.lineEdit.isEnabled():
                break
            elif not self.addCityDialog.lineEdit.isEnabled() and self.addCityDialog.lineEdit.text() == '':
                messageBox = QtWidgets.QMessageBox()
                messageBox.setWindowTitle('Ошибка')
                messageBox.addButton('Ок', 5)
                messageBox.setText('Не было введено наименование города!')
                messageBox.exec()
            else:
                with engine.connect() as conn:
                    query = (select(func.count()).where(City.name == self.addCityDialog.lineEdit.text()))
                    if conn.execute(query).all()[0][0] > 0:
                        messageBox = QtWidgets.QMessageBox()
                        messageBox.setWindowTitle('Ошибка')
                        messageBox.addButton('Ок', 5)
                        messageBox.setText('Город \"' + self.addCityDialog.lineEdit.text() + '\" уже существует!')
                        messageBox.exec()
                        conn.close()
                    else:
                        conn.execute(
                            insert(City),
                            [
                                {'name': self.addCityDialog.lineEdit.text()},
                            ]
                        )
                        conn.close()
                        self.updateData()
                        break

    def renameButtonClicked(self):
        if len(self.listOfCities.selectedItems()) == 1:
            self.renameCityDialog = RenameCityDialog(self.listOfCities.item(self.listOfCities.currentRow(), 0).text())
            while True:
                self.renameCityDialog.lineEdit.setEnabled(True)
                self.renameCityDialog.exec()
                if self.renameCityDialog.lineEdit.isEnabled():
                    break
                elif not self.renameCityDialog.lineEdit.isEnabled() and self.renameCityDialog.lineEdit.text() == '':
                    messageBox = QtWidgets.QMessageBox()
                    messageBox.setWindowTitle('Ошибка')
                    messageBox.addButton('Ок', 5)
                    messageBox.setText('Не было введено наименование города!')
                    messageBox.exec()
                else:
                    with engine.connect() as conn:
                        query = (select(func.count()).
                                  where(City.name == self.renameCityDialog.lineEdit.text()).
                                  where(City.id != self.listOfCities.item(self.listOfCities.currentRow(), 0).data(1)))
                        if conn.execute(query).all()[0][0] > 0:
                            messageBox = QtWidgets.QMessageBox()
                            messageBox.setWindowTitle('Ошибка')
                            messageBox.addButton('Ок', 5)
                            messageBox.setText('Город \"' + self.renameCityDialog.lineEdit.text() + '\" уже существует!')
                            messageBox.exec()
                            conn.close()
                        else:
                            conn.execute(
                                update(City).values(name = self.renameCityDialog.lineEdit.text()).
                                    where(City.id == self.listOfCities.item(self.listOfCities.currentRow(), 0).data(1))
                            )
                            conn.close()
                            self.updateData()
                            break

    def deleteButtonClicked(self):
        if self.listOfCities.currentRow() > -1:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setWindowTitle('Удаление города')
            messageBox.addButton('Удалить', 5)
            messageBox.addButton('Отменить', 6)
            messageBox.setText('Удалить город \"' +
                               self.listOfCities.item(self.listOfCities.currentRow(), 0).text() + '\"?')
            reply = messageBox.exec()
            if reply == 0:
                with engine.connect() as conn:
                    query = (select(func.count()).
                              where(City.id == self.listOfCities.item(self.listOfCities.currentRow(), 0).data(1)))
                    if conn.execute(query).all()[0][0] != 1:
                        messageBox = QtWidgets.QMessageBox()
                        messageBox.setWindowTitle('Ошибка')
                        messageBox.addButton('Ок', 5)
                        messageBox.setText('Города \"' +
                                           self.listOfCities.item(self.listOfCities.currentRow(), 0).text() +
                                           '\" не существует!')
                        messageBox.exec()
                        conn.close()
                    else:
                        conn.execute(
                            delete(City).where(City.id ==
                                               self.listOfCities.item(self.listOfCities.currentRow(), 0).data(1))
                        )
                        conn.close()
                        self.updateData()

    def changeEnableButtons(self):
        if len(self.listOfCities.selectedItems()) != 1:
            self.renameButton.setEnabled(False)
            self.deleteButton.setEnabled(False)
        else:
            self.renameButton.setEnabled(True)
            self.deleteButton.setEnabled(True)