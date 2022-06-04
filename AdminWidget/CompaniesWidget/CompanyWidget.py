from PyQt5 import QtWidgets
from declaration import engine
from AdminWidget.CompaniesWidget.AddCompanyDialog import AddCompanyDialog
from AdminWidget.CompaniesWidget.ChangeCompanyDialog import ChangeCompanyDialog
from sqlalchemy import select, func, insert, update, delete
from Models.Company import Company

class CompaniesWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(CompaniesWidget, self).__init__(*args, **kwargs)
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
        self.listCompanies = QtWidgets.QTableWidget()
        self.listCompanies.setEditTriggers(self.listCompanies.EditTrigger.NoEditTriggers)
        self.listCompanies.setSelectionMode(self.listCompanies.SelectionMode.SingleSelection)
        self.listCompanies.setSelectionBehavior(self.listCompanies.SelectionBehavior.SelectRows)
        self.listCompanies.setColumnCount(3)
        self.listCompanies.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem('Наименование'))
        self.listCompanies.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem('Страна'))
        self.listCompanies.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem('Год основания'))
        self.listCompanies.pressed.connect(self.changeEnableButtons)
        self.vBoxLayout.addWidget(self.listCompanies)
        self.vBoxLayout.addWidget(self.widgetWithButtons)
        self.setLayout(self.vBoxLayout)
        self.updateData()

    def updateData(self):
        self.listCompanies.setRowCount(0)
        with engine.connect() as conn:
            index = 0
            querry = (select(Company).order_by(Company.name, Company.country, Company.yearOfEstablishment))
            for row in conn.execute(querry):
                item = QtWidgets.QTableWidgetItem(row[1])
                item.setData(1, row[0])
                self.listCompanies.insertRow(index)
                self.listCompanies.setItem(index, 0, item)
                item1 = QtWidgets.QTableWidgetItem(str(row[2]))
                self.listCompanies.setItem(index, 1, item1)
                item2 = QtWidgets.QTableWidgetItem(str(row[3]))
                self.listCompanies.setItem(index, 2, item2)
                index += 1
        self.changeEnableButtons()

    def addButtonClicked(self):
        self.addCompanyDialog = AddCompanyDialog()
        while True:
            self.addCompanyDialog.lineEdit.setEnabled(True)
            self.addCompanyDialog.exec()
            if self.addCompanyDialog.lineEdit.isEnabled():
                break
            elif not self.addCompanyDialog.lineEdit.isEnabled() and self.addCompanyDialog.lineEdit.text() == '':
                messageBox = QtWidgets.QMessageBox()
                messageBox.setWindowTitle('Ошибка')
                messageBox.addButton('Ок', 5)
                messageBox.setText('Не было введено наименование киностудии!')
                messageBox.exec()
            elif not self.addCompanyDialog.lineEdit.isEnabled() and self.addCompanyDialog.lineEdit1.text() == '':
                messageBox = QtWidgets.QMessageBox()
                messageBox.setWindowTitle('Ошибка')
                messageBox.addButton('Ок', 5)
                messageBox.setText('Не была введена страна!')
                messageBox.exec()
            else:
                with engine.connect() as conn:
                    conn.execute(
                        insert(Company),
                        [
                            {'name': self.addCompanyDialog.lineEdit.text(),
                             'country': self.addCompanyDialog.lineEdit1.text(),
                             'yearOfEstablishment': self.addCompanyDialog.yearOfEstablishment.value()},
                        ]
                    )
                    conn.close()
                    self.updateData()
                    break

    def changeButtonClicked(self):
        if len(self.listCompanies.selectedItems()) == 3:
            self.changeCompanyDialog = ChangeCompanyDialog(
                self.listCompanies.item(self.listCompanies.currentRow(), 0).text(),
                self.listCompanies.item(self.listCompanies.currentRow(), 1).text(),
                int(self.listCompanies.item(self.listCompanies.currentRow(), 2).text()))
            while True:
                self.changeCompanyDialog.lineEdit.setEnabled(True)
                self.changeCompanyDialog.exec()
                if self.changeCompanyDialog.lineEdit.isEnabled():
                    break
                elif not self.changeCompanyDialog.lineEdit.isEnabled() \
                        and self.changeCompanyDialog.lineEdit.text() == '':
                    messageBox = QtWidgets.QMessageBox()
                    messageBox.setWindowTitle('Ошибка')
                    messageBox.addButton('Ок', 5)
                    messageBox.setText('Не было введено наименование киностудии!')
                    messageBox.exec()
                elif not self.changeCompanyDialog.lineEdit.isEnabled() \
                         and self.changeCompanyDialog.lineEdit1.text() == '':
                    messageBox = QtWidgets.QMessageBox()
                    messageBox.setWindowTitle('Ошибка')
                    messageBox.addButton('Ок', 5)
                    messageBox.setText('Не была введена страна!!')
                    messageBox.exec()
                else:
                    with engine.connect() as conn:
                        conn.execute(
                            update(Company).values(
                                name = self.changeCompanyDialog.lineEdit.text(),
                                country = self.changeCompanyDialog.lineEdit1.text(),
                                yearOfEstablishment = self.changeCompanyDialog.yearOfEstablishment.value()).
                                where(Company.id ==
                                      self.listCompanies.item(self.listCompanies.currentRow(), 0).data(1))
                        )
                        conn.close()
                        self.updateData()
                        break

    def deleteButtonClicked(self):
        if self.listCompanies.currentRow() > -1:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setWindowTitle('Удаление киностудии')
            messageBox.addButton('Удалить', 5)
            messageBox.addButton('Отменить', 6)
            messageBox.setText('Удалить киностудию \"'
                               + self.listCompanies.item(self.listCompanies.currentRow(), 0).text() + '\"?')
            reply = messageBox.exec()
            if reply == 0:
                with engine.connect() as conn:
                    query = (select(func.count())
                              .where(Company.id ==
                                     self.listCompanies.item(self.listCompanies.currentRow(), 0).data(1)))
                    if conn.execute(query).all()[0][0] != 1:
                        messageBox = QtWidgets.QMessageBox()
                        messageBox.setWindowTitle('Ошибка')
                        messageBox.addButton('Ок', 5)
                        messageBox.setText('Киностудии \"' +
                                           self.listCompanies.item(self.listCompanies.currentRow(), 0).text() +
                                           '\" не существует!')
                        messageBox.exec()
                        conn.close()
                    else:
                        conn.execute(
                            delete(Company).
                                where(Company.id ==
                                      self.listCompanies.item(self.listCompanies.currentRow(), 0).data(1))
                        )
                        conn.close()
                        self.updateData()

    def changeEnableButtons(self):
        if len(self.listCompanies.selectedItems()) != 3:
            self.changeButton.setEnabled(False)
            self.deleteButton.setEnabled(False)
        else:
            self.changeButton.setEnabled(True)
            self.deleteButton.setEnabled(True)