from PyQt5 import QtWidgets
from declaration import engine
from sqlalchemy import select, func, insert, update, delete
from Models.Worker import Worker

class ListOfWorkersWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(ListOfWorkersWidget, self).__init__(*args, **kwargs)
        self.changeButton = QtWidgets.QPushButton('Изменить статус')
        self.changeButton.clicked.connect(self.changeButtonClicked)
        self.deleteButton = QtWidgets.QPushButton('Удалить')
        self.deleteButton.clicked.connect(self.deleteButtonClicked)
        self.hBoxLayout = QtWidgets.QHBoxLayout()
        self.hBoxLayout.addWidget(self.changeButton)
        self.hBoxLayout.addWidget(self.deleteButton)
        self.widgetWithButtons = QtWidgets.QWidget()
        self.widgetWithButtons.setLayout(self.hBoxLayout)
        self.vBoxLayout = QtWidgets.QVBoxLayout()
        self.listOfWorkers = QtWidgets.QTableWidget()
        self.listOfWorkers.setEditTriggers(self.listOfWorkers.EditTrigger.NoEditTriggers)
        self.listOfWorkers.setSelectionMode(self.listOfWorkers.SelectionMode.SingleSelection)
        self.listOfWorkers.setSelectionBehavior(self.listOfWorkers.SelectionBehavior.SelectRows)
        self.listOfWorkers.setColumnCount(5)
        self.listOfWorkers.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem('Фамилия'))
        self.listOfWorkers.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem('Имя'))
        self.listOfWorkers.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem('Отчество'))
        self.listOfWorkers.setHorizontalHeaderItem(3, QtWidgets.QTableWidgetItem('Почта'))
        self.listOfWorkers.setHorizontalHeaderItem(4, QtWidgets.QTableWidgetItem('Статус'))
        self.listOfWorkers.pressed.connect(self.changeEnableButtons)
        self.vBoxLayout.addWidget(self.listOfWorkers)
        self.vBoxLayout.addWidget(self.widgetWithButtons)
        self.setLayout(self.vBoxLayout)
        self.updateData()

    def updateData(self):
        self.listOfWorkers.setRowCount(0)
        with engine.connect() as conn:
            index = 0
            query = (select(Worker).where(Worker.right != 'admin')
                      .order_by(Worker.surname, Worker.name, Worker.patronymic, Worker.mail, Worker.right))
            for row in conn.execute(query):
                item = QtWidgets.QTableWidgetItem(row[2])
                item.setData(1, row[0])
                self.listOfWorkers.insertRow(index)
                self.listOfWorkers.setItem(index, 0, item)
                item1 = QtWidgets.QTableWidgetItem(row[1])
                self.listOfWorkers.setItem(index, 1, item1)
                item2 = QtWidgets.QTableWidgetItem(row[3])
                self.listOfWorkers.setItem(index, 2, item2)
                item3 = QtWidgets.QTableWidgetItem(row[6])
                self.listOfWorkers.setItem(index, 3, item3)
                item4 = QtWidgets.QTableWidgetItem('Заблокирован' if row[8] == 'lockedWorker' else 'Разблокирован')
                self.listOfWorkers.setItem(index, 4, item4)
                index += 1
        self.changeEnableButtons()

    def changeButtonClicked(self):
        if len(self.listOfWorkers.selectedItems()) == 5:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setWindowTitle('Изменение статуса')
            messageBox.addButton('Разблокировать' if self.listOfWorkers.item(self.listOfWorkers.currentRow(), 4).text()
                                  == 'Заблокирован' else 'Заблокировать', 5)
            messageBox.addButton('Отменить', 6)
            messageBox.setText('Разблокировать'
                               + ' сотрудника \"' + self.listOfWorkers.item(self.listOfWorkers.currentRow(),
                                                                            0).text() + ' '
                               + self.listOfWorkers.item(self.listOfWorkers.currentRow(), 1).text() + ' '
                               + self.listOfWorkers.item(self.listOfWorkers.currentRow(), 2).text() + '\"?'
                               if self.listOfWorkers.item(self.listOfWorkers.currentRow(), 4).text()
                                  == 'Заблокирован' else 'Заблокировать'
                                                         + ' сотрудника \"'+ self.listOfWorkers
                               .item(self.listOfWorkers.currentRow(), 0).text() + ' ' + self.listOfWorkers
                               .item(self.listOfWorkers.currentRow(), 1).text() + ' ' + self.listOfWorkers
                               .item(self.listOfWorkers.currentRow(), 2).text() + '\"?')
            reply = messageBox.exec()
            if reply == 0:
                with engine.connect() as conn:
                    query = (select(Worker)
                             .where(Worker.id == self.listOfWorkers.item(self.listOfWorkers.currentRow(), 0).data(1)))
                    if conn.execute(query).all()[0][8] == 'lockedWorker':
                        conn.execute(update(Worker).values(right = 'unlockedWorker')
                                     .where(Worker.id == self.listOfWorkers.item
                        (self.listOfWorkers.currentRow(), 0).data(1)))
                    elif conn.execute(query).all()[0][8] == 'unlockedWorker':
                        conn.execute(update(Worker).values(right='lockedWorker')
                                     .where(Worker.id == self.listOfWorkers.item
                        (self.listOfWorkers.currentRow(), 0).data(1)))
                    conn.close()
                    self.updateData()

    def deleteButtonClicked(self):
        if len(self.listOfWorkers.selectedItems()) == 5:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setWindowTitle('Изменение статуса')
            messageBox.addButton('Удалить', 5)
            messageBox.addButton('Отменить', 6)
            messageBox.setText('Удалить сотрудника \"' + self.listOfWorkers.item(
                self.listOfWorkers.currentRow(), 0).text() + ' '
                                                         + self.listOfWorkers.item(self.listOfWorkers.currentRow(),
                                                                                   1).text() + ' '
                                                         + self.listOfWorkers.item(self.listOfWorkers.currentRow(),
                                                                                   2).text() + '\"?')
            reply = messageBox.exec()
            if reply == 0:
                with engine.connect() as conn:
                    query = (select(Worker)
                             .where(Worker.id == self.listOfWorkers.item(self.listOfWorkers.currentRow(), 0).data(1)))
                    if len(conn.execute(query).all()) == 1:
                        conn.execute(delete(Worker)
                                     .where(Worker.id == self.listOfWorkers.item
                        (self.listOfWorkers.currentRow(), 0).data(1)))
                        conn.close()
                        self.updateData()
                    else:
                        messageBox = QtWidgets.QMessageBox()
                        messageBox.setWindowTitle('Ошибка')
                        messageBox.addButton('Ок', 5)
                        messageBox.setText('Cотрудника \"' + self.listOfWorkers.item(
                            self.listOfWorkers.currentRow(), 0).text() + ' '
                                           + self.listOfWorkers.item(self.listOfWorkers.currentRow(),
                                                                     1).text() + ' '
                                           + self.listOfWorkers.item(self.listOfWorkers.currentRow(),
                                                                     2).text() + '\" не существует!')
                        messageBox.exec()

    def changeEnableButtons(self):
        if len(self.listOfWorkers.selectedItems()) != 5:
            self.changeButton.setEnabled(False)
            self.deleteButton.setEnabled(False)
        else:
            self.changeButton.setEnabled(True)
            self.deleteButton.setEnabled(True)