from PyQt5 import QtWidgets
from declaration import engine
from AdminWidget.TypesOfHallWidget.AddTypeOfHallDialog import AddTypeOfHallDialog
from AdminWidget.TypesOfHallWidget.ChangeTypeOfHallDialog import ChangeTypeOfHallDialog
from sqlalchemy import select, func, insert, update, delete
from Models.TypeOfHall import TypeOfHall
from Models.Hall import Hall
from Models.Seat import Seat

class TypesOfHallWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(TypesOfHallWidget, self).__init__(*args, **kwargs)
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
        self.listOfTypesOfHall = QtWidgets.QTableWidget()
        self.listOfTypesOfHall.setEditTriggers(self.listOfTypesOfHall.EditTrigger.NoEditTriggers)
        self.listOfTypesOfHall.setSelectionMode(self.listOfTypesOfHall.SelectionMode.SingleSelection)
        self.listOfTypesOfHall.setSelectionBehavior(self.listOfTypesOfHall.SelectionBehavior.SelectRows)
        self.listOfTypesOfHall.setColumnCount(3)
        self.listOfTypesOfHall.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem('Наименование'))
        self.listOfTypesOfHall.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem('Количество рядов'))
        self.listOfTypesOfHall.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem('Количество мест'))
        self.listOfTypesOfHall.pressed.connect(self.changeEnableButtons)
        self.vBoxLayout.addWidget(self.listOfTypesOfHall)
        self.vBoxLayout.addWidget(self.widgetWithButtons)
        self.setLayout(self.vBoxLayout)
        self.updateData()

    def updateData(self):
        self.listOfTypesOfHall.setRowCount(0)
        with engine.connect() as conn:
            index = 0
            querry = (select(TypeOfHall).order_by(TypeOfHall.type))
            for row in conn.execute(querry):
                item = QtWidgets.QTableWidgetItem(row[1])
                item.setData(1, row[0])
                self.listOfTypesOfHall.insertRow(index)
                self.listOfTypesOfHall.setItem(index, 0, item)
                item1 = QtWidgets.QTableWidgetItem(str(row[2]))
                self.listOfTypesOfHall.setItem(index, 1, item1)
                item2 = QtWidgets.QTableWidgetItem(str(row[3]))
                self.listOfTypesOfHall.setItem(index, 2, item2)
                index += 1
        self.changeEnableButtons()

    def addButtonClicked(self):
        self.addTypeOfHallDialog = AddTypeOfHallDialog()
        while True:
            self.addTypeOfHallDialog.lineEdit.setEnabled(True)
            self.addTypeOfHallDialog.exec()
            if self.addTypeOfHallDialog.lineEdit.isEnabled():
                break
            elif not self.addTypeOfHallDialog.lineEdit.isEnabled() and self.addTypeOfHallDialog.lineEdit.text() == '':
                messageBox = QtWidgets.QMessageBox()
                messageBox.setWindowTitle('Ошибка')
                messageBox.addButton('Ок', 5)
                messageBox.setText('Не было введен тип зала!')
                messageBox.exec()
            else:
                with engine.connect() as conn:
                    querry = (select(func.count()).where(TypeOfHall.type == self.addTypeOfHallDialog.lineEdit.text()))
                    querry1 = (select(func.count()).
                               where(TypeOfHall.countRow == self.addTypeOfHallDialog.countOfRows.value()).
                               where(TypeOfHall.countCol == self.addTypeOfHallDialog.countOfColumns.value()))
                    if conn.execute(querry).all()[0][0] > 0:
                        messageBox = QtWidgets.QMessageBox()
                        messageBox.setWindowTitle('Ошибка')
                        messageBox.addButton('Ок', 5)
                        messageBox.setText('Тип зала \"' +
                                           self.addTypeOfHallDialog.lineEdit.text() + '\" уже существует!')
                        messageBox.exec()
                        conn.close()
                    elif conn.execute(querry1).all()[0][0] > 0:
                        messageBox = QtWidgets.QMessageBox()
                        messageBox.setWindowTitle('Ошибка')
                        messageBox.addButton('Ок', 5)
                        messageBox.setText('Тип зала с таким количеством и расположением мест уже существует!')
                        messageBox.exec()
                        conn.close()
                    else:
                        conn.execute(
                            insert(TypeOfHall),
                            [
                                {'type': self.addTypeOfHallDialog.lineEdit.text(),
                                 'countRow': self.addTypeOfHallDialog.countOfRows.value(),
                                 'countCol': self.addTypeOfHallDialog.countOfColumns.value()},
                            ]
                        )
                        conn.close()
                        self.updateData()
                        break

    def changeButtonClicked(self):
        if len(self.listOfTypesOfHall.selectedItems()) == 3:
            self.changeTypeOfHallDialog = ChangeTypeOfHallDialog(
            self.listOfTypesOfHall.item(self.listOfTypesOfHall.currentRow(), 0).text(),
                int(self.listOfTypesOfHall.item(self.listOfTypesOfHall.currentRow(), 1).text()),
                int(self.listOfTypesOfHall.item(self.listOfTypesOfHall.currentRow(), 2).text()))
            while True:
                self.changeTypeOfHallDialog.lineEdit.setEnabled(True)
                self.changeTypeOfHallDialog.exec()
                if self.changeTypeOfHallDialog.lineEdit.isEnabled():
                    break
                elif not self.changeTypeOfHallDialog.lineEdit.isEnabled() \
                        and self.changeTypeOfHallDialog.lineEdit.text() == '':
                    messageBox = QtWidgets.QMessageBox()
                    messageBox.setWindowTitle('Ошибка')
                    messageBox.addButton('Ок', 5)
                    messageBox.setText('Не был введен тип зала!')
                    messageBox.exec()
                else:
                    with engine.connect() as conn:
                        query = (select(func.count()).
                                 where(TypeOfHall.type == self.changeTypeOfHallDialog.lineEdit.text()).
                                 where(TypeOfHall.id != self.listOfTypesOfHall.item(
                            self.listOfTypesOfHall.currentRow(), 0).data(1)))
                        query1 = (select(func.count()).
                                  where(TypeOfHall.countRow == self.changeTypeOfHallDialog.countOfRows.value()).
                                  where(TypeOfHall.countCol == self.changeTypeOfHallDialog.countOfColumns.value()).
                                  where(TypeOfHall.id != self.listOfTypesOfHall.item(
                                  self.listOfTypesOfHall.currentRow(), 0).data(1)))
                        if conn.execute(query).all()[0][0] > 0:
                            messageBox = QtWidgets.QMessageBox()
                            messageBox.setWindowTitle('Ошибка')
                            messageBox.addButton('Ок', 5)
                            messageBox.setText('Тип зала \"' +
                                               self.changeTypeOfHallDialog.lineEdit.text() + '\" уже существует!')
                            messageBox.exec()
                            conn.close()
                        elif conn.execute(query1).all()[0][0] > 0:
                            messageBox = QtWidgets.QMessageBox()
                            messageBox.setWindowTitle('Ошибка')
                            messageBox.addButton('Ок', 5)
                            messageBox.setText('Тип зала с таким количеством и расположением мест уже существует!')
                            messageBox.exec()
                            conn.close()
                        else:
                            conn.execute(
                                update(TypeOfHall).values(
                                    type = self.changeTypeOfHallDialog.lineEdit.text(),
                                    countRow = self.changeTypeOfHallDialog.countOfRows.value(),
                                    countCol = self.changeTypeOfHallDialog.countOfColumns.value()).
                                    where(TypeOfHall.id ==
                                          self.listOfTypesOfHall.item(self.listOfTypesOfHall.currentRow(), 0).data(1))
                            )
                            '''query2 = (select(Hall).where(Hall.idTypeOfHall == TypeOfHall.id))
                            for i in range(len(conn.execute(query2).all())):
                                query3 = (select(Hall).where(Hall.id == conn.execute(query2).all()[i][0]))
                                query4 = (select(Seat).where(Seat.id == conn.execute(query3).all()[0][0]))
                                for j in range(len(conn.execute(query4).all())):
                                    conn.execute(delete(Seat).where(Seat.id == conn.execute(query4).all()[j][0]))
                                for j in range(self.changeTypeOfHallDialog.countOfRows.value()):
                                    for k in range(self.changeTypeOfHallDialog.countOfColumns.value()):
                                        conn.execute(
                                            insert(Seat),
                                            [
                                                {
                                                    'numberRow': j,
                                                    'numberCol': k,
                                                    'idHall': conn.execute(query3).all()[0][0]
                                                }
                                            ]
                                        )'''
                            conn.close()
                            self.updateData()
                            break

    def deleteButtonClicked(self):
        if self.listOfTypesOfHall.currentRow() > -1:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setWindowTitle('Удаление типа зала')
            messageBox.addButton('Удалить', 5)
            messageBox.addButton('Отменить', 6)
            messageBox.setText('Удалить тип зала \"' +
                               self.listOfTypesOfHall.item(self.listOfTypesOfHall.currentRow(), 0).text() + '\"?')
            reply = messageBox.exec()
            if reply == 0:
                with engine.connect() as conn:
                    querry = (select(func.count()).
                              where(TypeOfHall.id ==
                                    self.listOfTypesOfHall.item(self.listOfTypesOfHall.currentRow(), 0).data(1)))
                    if conn.execute(querry).all()[0][0] != 1:
                        messageBox = QtWidgets.QMessageBox()
                        messageBox.setWindowTitle('Ошибка')
                        messageBox.addButton('Ок', 5)
                        messageBox.setText('Типа зала \"' +
                                           self.listOfTypesOfHall.item(self.listOfTypesOfHall.currentRow(), 0).text() +
                                           '\" не существует!')
                        messageBox.exec()
                        conn.close()
                    else:
                        conn.execute(
                            delete(TypeOfHall).
                                where(TypeOfHall.id ==
                                      self.listOfTypesOfHall.item(self.listOfTypesOfHall.currentRow(), 0).data(1))
                        )
                        conn.close()
                        self.updateData()

    def changeEnableButtons(self):
        if len(self.listOfTypesOfHall.selectedItems()) != 3:
            self.changeButton.setEnabled(False)
            self.deleteButton.setEnabled(False)
        else:
            self.changeButton.setEnabled(True)
            self.deleteButton.setEnabled(True)