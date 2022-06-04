from PyQt5 import QtWidgets
from declaration import engine
from WorkersWidget.FilmsWidget.AddFilmDialog import AddFilmDialog
from WorkersWidget.FilmsWidget.ChangeFilmDialog import ChangeFilmDialog
from sqlalchemy import select, func, insert, update, delete
from Models.Film import Film
from Models.Company import Company

class FilmsWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(FilmsWidget, self).__init__(*args, **kwargs)
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
        self.listOfFilms = QtWidgets.QTableWidget()
        self.listOfFilms.setEditTriggers(self.listOfFilms.EditTrigger.NoEditTriggers)
        self.listOfFilms.setSelectionMode(self.listOfFilms.SelectionMode.SingleSelection)
        self.listOfFilms.setSelectionBehavior(self.listOfFilms.SelectionBehavior.SelectRows)
        self.listOfFilms.setColumnCount(4)
        self.listOfFilms.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem('Название'))
        self.listOfFilms.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem('Продолжительность'))
        self.listOfFilms.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem('ВОзрастное ограничение'))
        self.listOfFilms.setHorizontalHeaderItem(3, QtWidgets.QTableWidgetItem('Киностудия'))
        self.listOfFilms.pressed.connect(self.changeEnableButtons)
        self.vBoxLayout.addWidget(self.listOfFilms)
        self.vBoxLayout.addWidget(self.widgetWithButtons)
        self.setLayout(self.vBoxLayout)
        self.updateData()

    def updateData(self):
        self.listOfFilms.setRowCount(0)
        with engine.connect() as conn:
            index = 0
            query = (select(Film.id, Film.name, Film.duration,
                            Film.ageLimit, Company.id, Company.name)
                     .join(Company, Company.id == Film.idCompany)
                     .order_by(Film.name, Film.duration, Film.ageLimit, Company.name))
            for row in conn.execute(query):
                item = QtWidgets.QTableWidgetItem(row[1])
                item.setData(1, row[0])
                self.listOfFilms.insertRow(index)
                self.listOfFilms.setItem(index, 0, item)
                item1 = QtWidgets.QTableWidgetItem(str(row[2]))
                self.listOfFilms.setItem(index, 1, item1)
                item2 = QtWidgets.QTableWidgetItem(str(row[3]))
                self.listOfFilms.setItem(index, 2, item2)
                item3 = QtWidgets.QTableWidgetItem(str(row[5]))
                item3.setData(1, row[4])
                self.listOfFilms.setItem(index, 3, item3)
                index += 1
        self.changeEnableButtons()

    def addButtonClicked(self):
        query = (select(Company.id, Company.name).order_by(Company.name))
        listOfCompanies = []
        with engine.connect() as conn:
            for row in conn.execute(query):
                listOfCompanies.append((row[0], row[1]))
            conn.close()
        self.addFilmDialog = AddFilmDialog(listOfCompanies)
        while True:
            self.addFilmDialog.lineEdit.setEnabled(True)
            self.addFilmDialog.exec()
            if self.addFilmDialog.lineEdit.isEnabled():
                break
            elif not self.addFilmDialog.lineEdit.isEnabled() and self.addFilmDialog.lineEdit.text() == '':
                messageBox = QtWidgets.QMessageBox()
                messageBox.setWindowTitle('Ошибка')
                messageBox.addButton('Ок', 5)
                messageBox.setText('Не было введено название фильма!')
                messageBox.exec()
            else:
                query = (select(func.count()).
                                where(Company.id == self.addFilmDialog.listOfCompanies.itemData(
                    self.addFilmDialog.listOfCompanies.currentIndex(), 1)))
                with engine.connect() as conn:
                    if conn.execute(query).all()[0][0] != 1:
                        messageBox = QtWidgets.QMessageBox()
                        messageBox.setWindowTitle('Ошибка')
                        messageBox.addButton('Ок', 5)
                        messageBox.setText('Выбранной киностудии не существует!')
                        messageBox.exec()
                        conn.close()
                    else:
                        conn.execute(
                            insert(Film),
                            [
                                {'name': self.addFilmDialog.lineEdit.text(),
                                 'duration': self.addFilmDialog.duration.time().toPyTime(),
                                 'ageLimit': self.addFilmDialog.ageLimit.value(),
                                 'idCompany': self.addFilmDialog.listOfCompanies.itemData(
                                     self.addFilmDialog.listOfCompanies.currentIndex(), 1)},
                            ]
                        )
                        conn.close()
                        self.updateData()
                        break

    def changeButtonClicked(self):
        if len(self.listOfFilms.selectedItems()) == 4:
            query = (select(Company.id, Company.name).order_by(Company.name))
            listOfCompanies = []
            with engine.connect() as conn:
                for row in conn.execute(query):
                    listOfCompanies.append((row[0], row[1]))
                conn.close()
            self.changeFilmDialog = ChangeFilmDialog(
                listOfCompanies,
                self.listOfFilms.item(self.listOfFilms.currentRow(), 0).text(),
                self.listOfFilms.item(self.listOfFilms.currentRow(), 1).text(),
                self.listOfFilms.item(self.listOfFilms.currentRow(), 2).text(),
                self.listOfFilms.item(self.listOfFilms.currentRow(), 3).data(1))
            while True:
                self.changeFilmDialog.lineEdit.setEnabled(True)
                self.changeFilmDialog.exec()
                if self.changeFilmDialog.lineEdit.isEnabled():
                    break
                elif not self.changeFilmDialog.lineEdit.isEnabled() \
                        and self.changeFilmDialog.lineEdit.text() == '':
                    messageBox = QtWidgets.QMessageBox()
                    messageBox.setWindowTitle('Ошибка')
                    messageBox.addButton('Ок', 5)
                    messageBox.setText('Не было введено название фильма!')
                    messageBox.exec()
                else:
                    with engine.connect() as conn:
                            conn.execute(
                                update(Film)
                                    .values(name=self.changeFilmDialog.lineEdit.text(),
                                            duration=self.changeFilmDialog.duration.time().toPyTime(),
                                            ageLimit = self.changeFilmDialog.ageLimit.value(),
                                            idCompany=self.changeFilmDialog.listOfCompanies.itemData(
                                                self.changeFilmDialog.listOfCompanies.currentIndex(), 1))
                                    .where(Film.id == self.listOfFilms.item(self.listOfFilms.currentRow(), 0).data(1))
                            )
                            conn.close()
                            self.updateData()
                            break

    def deleteButtonClicked(self):
        if self.listOfFilms.currentRow() > -1:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setWindowTitle('Удаление фильма')
            messageBox.addButton('Удалить', 5)
            messageBox.addButton('Отменить', 6)
            messageBox.setText('Удалить фильм \"'
                               + self.listOfFilms.item(self.listOfFilms.currentRow(), 0).text() + '\"?')
            reply = messageBox.exec()
            if reply == 0:
                with engine.connect() as conn:
                    query = (select(func.count())
                             .where(Film.id ==
                                    self.listOfFilms.item(self.listOfFilms.currentRow(), 0).data(1)))
                    if conn.execute(query).all()[0][0] != 1:
                        messageBox = QtWidgets.QMessageBox()
                        messageBox.setWindowTitle('Ошибка')
                        messageBox.addButton('Ок', 5)
                        messageBox.setText('Фильм \"'
                                           + self.listOfFilms.item(self.listOfFilms.currentRow(), 0).text()
                                           + '\" не существует!')
                        messageBox.exec()
                        conn.close()
                    else:
                        conn.execute(
                            delete(Film)
                                .where(Film.id == self.listOfFilms.item(self.listOfFilms.currentRow(), 0).data(1))
                        )
                        conn.close()
                        self.updateData()

    def changeEnableButtons(self):
        if len(self.listOfFilms.selectedItems()) != 4:
            self.changeButton.setEnabled(False)
            self.deleteButton.setEnabled(False)
        else:
            self.changeButton.setEnabled(True)
            self.deleteButton.setEnabled(True)