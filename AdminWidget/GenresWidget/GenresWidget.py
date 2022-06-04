from PyQt5 import QtWidgets
from declaration import engine
from AdminWidget.GenresWidget.AddGenreDialog import AddGenreDialog
from AdminWidget.GenresWidget.RenameGenreDialog import RenameGenreDialog
from sqlalchemy import select, func, insert, update, delete
from Models.Genre import Genre

class GenresWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(GenresWidget, self).__init__(*args, **kwargs)
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
        self.listOfGenres = QtWidgets.QTableWidget()
        self.listOfGenres.setEditTriggers(self.listOfGenres.EditTrigger.NoEditTriggers)
        self.listOfGenres.setSelectionMode(self.listOfGenres.SelectionMode.SingleSelection)
        self.listOfGenres.setSelectionBehavior(self.listOfGenres.SelectionBehavior.SelectRows)
        self.listOfGenres.setColumnCount(1)
        self.listOfGenres.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem('Наименование'))
        self.listOfGenres.pressed.connect(self.changeEnableButtons)
        self.vBoxLayout.addWidget(self.listOfGenres)
        self.vBoxLayout.addWidget(self.widgetWithButtons)
        self.setLayout(self.vBoxLayout)
        self.updateData()

    def updateData(self):
        self.listOfGenres.setRowCount(0)
        with engine.connect() as conn:
            index = 0
            query = (select(Genre).order_by(Genre.name))
            for row in conn.execute(query):
                item = QtWidgets.QTableWidgetItem(row[1])
                item.setData(1, row[0])
                self.listOfGenres.insertRow(index)
                self.listOfGenres.setItem(index, 0, item)
                index += 1
        self.changeEnableButtons()

    def addButtonClicked(self):
        self.addGenreDialog = AddGenreDialog()
        while True:
            self.addGenreDialog.lineEdit.setEnabled(True)
            self.addGenreDialog.exec()
            if self.addGenreDialog.lineEdit.isEnabled():
                break
            elif not self.addGenreDialog.lineEdit.isEnabled() and self.addGenreDialog.lineEdit.text() == '':
                messageBox = QtWidgets.QMessageBox()
                messageBox.setWindowTitle('Ошибка')
                messageBox.addButton('Ок', 5)
                messageBox.setText('Не было введено наименование жанр!')
                messageBox.exec()
            else:
                with engine.connect() as conn:
                    query = (select(func.count()).where(Genre.name == self.addGenreDialog.lineEdit.text()))
                    if conn.execute(query).all()[0][0] > 0:
                        messageBox = QtWidgets.QMessageBox()
                        messageBox.setWindowTitle('Ошибка')
                        messageBox.addButton('Ок', 5)
                        messageBox.setText('Жанр \"' + self.addGenreDialog.lineEdit.text() + '\" уже существует!')
                        messageBox.exec()
                        conn.close()
                    else:
                        conn.execute(
                            insert(Genre),
                            [
                                {'name': self.addGenreDialog.lineEdit.text()},
                            ]
                        )
                        conn.close()
                        self.updateData()
                        break

    def renameButtonClicked(self):
        if len(self.listOfGenres.selectedItems()) == 1:
            self.renameGenreDialog = RenameGenreDialog(self.listOfGenres.item(self.listOfGenres.currentRow(), 0).text())
            while True:
                self.renameGenreDialog.lineEdit.setEnabled(True)
                self.renameGenreDialog.exec()
                if self.renameGenreDialog.lineEdit.isEnabled():
                    break
                elif not self.renameGenreDialog.lineEdit.isEnabled() and self.renameGenreDialog.lineEdit.text() == '':
                    messageBox = QtWidgets.QMessageBox()
                    messageBox.setWindowTitle('Ошибка')
                    messageBox.addButton('Ок', 5)
                    messageBox.setText('Не было введено наименование жанра!')
                    messageBox.exec()
                else:
                    with engine.connect() as conn:
                        query = (select(func.count()).
                                  where(Genre.name == self.renameGenreDialog.lineEdit.text()).
                                  where(Genre.id != self.listOfGenres.item(self.listOfGenres.currentRow(), 0).data(1)))
                        if conn.execute(query).all()[0][0] > 0:
                            messageBox = QtWidgets.QMessageBox()
                            messageBox.setWindowTitle('Ошибка')
                            messageBox.addButton('Ок', 5)
                            messageBox.setText('Жанр \"'
                                               + self.renameGenreDialog.lineEdit.text() + '\" уже существует!')
                            messageBox.exec()
                            conn.close()
                        else:
                            conn.execute(
                                update(Genre).values(name = self.renameGenreDialog.lineEdit.text()).
                                    where(Genre.id == self.listOfGenres.item(self.listOfGenres.currentRow(), 0).data(1))
                            )
                            conn.close()
                            self.updateData()
                            break

    def deleteButtonClicked(self):
        if self.listOfGenres.currentRow() > -1:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setWindowTitle('Удаление жанра')
            messageBox.addButton('Удалить', 5)
            messageBox.addButton('Отменить', 6)
            messageBox.setText('Удалить жанр \"' +
                               self.listOfGenres.item(self.listOfGenres.currentRow(), 0).text() + '\"?')
            reply = messageBox.exec()
            if reply == 0:
                with engine.connect() as conn:
                    query = (select(func.count()).
                              where(Genre.id == self.listOfGenres.item(self.listOfGenres.currentRow(), 0).data(1)))
                    if conn.execute(query).all()[0][0] != 1:
                        messageBox = QtWidgets.QMessageBox()
                        messageBox.setWindowTitle('Ошибка')
                        messageBox.addButton('Ок', 5)
                        messageBox.setText('Жанра \"' +
                                           self.listOfGenres.item(self.listOfGenres.currentRow(), 0).text() +
                                           '\" не существует!')
                        messageBox.exec()
                        conn.close()
                    else:
                        conn.execute(
                            delete(Genre).where(Genre.id ==
                                               self.listOfGenres.item(self.listOfGenres.currentRow(), 0).data(1))
                        )
                        conn.close()
                        self.updateData()

    def changeEnableButtons(self):
        if len(self.listOfGenres.selectedItems()) != 1:
            self.renameButton.setEnabled(False)
            self.deleteButton.setEnabled(False)
        else:
            self.renameButton.setEnabled(True)
            self.deleteButton.setEnabled(True)