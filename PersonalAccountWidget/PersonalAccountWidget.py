from PyQt5 import QtWidgets, QtCore, Qt
from declaration import engine
from Models.Worker import Worker
from sqlalchemy import insert, select, func

class PersonalAccountWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(PersonalAccountWidget, self).__init__(*args, **kwargs)
        query = (select(Worker).where(Worker.id == self.parent().idWorker))
        with engine.connect() as conn:
            worker = conn.execute(query).all()[0]
            conn.close()
        self.label = QtWidgets.QLabel('Фамилия')
        self.label1 = QtWidgets.QLabel('Имя')
        self.label2 = QtWidgets.QLabel('Отчество')
        self.label3 = QtWidgets.QLabel('Пол')
        self.label4 = QtWidgets.QLabel('Дата рождения')
        self.label5 = QtWidgets.QLabel('Почта')
        self.label6 = QtWidgets.QLabel('Телефон')
        self.label7 = QtWidgets.QLabel('Серия паспорта')
        self.label8 = QtWidgets.QLabel('Номер паспорта')
        self.surname = QtWidgets.QLineEdit(worker[2])
        self.surname.setReadOnly(True)
        self.name = QtWidgets.QLineEdit(worker[1])
        self.surname.setReadOnly(True)
        self.patronymic = QtWidgets.QLineEdit(worker[3])
        self.patronymic.setReadOnly(True)
        self.gender = QtWidgets.QLineEdit()
        self.gender.setText('Мужской') if not worker[4] else self.gender.setText('Женский')
        self.gender.setReadOnly(True)
        self.dateBirthday = QtWidgets.QCalendarWidget()
        self.dateBirthday.setDateRange(worker[5], worker[5])
        self.dateBirthday.setSelectionMode(self.dateBirthday.SelectionMode.NoSelection)
        self.dateBirthday.setSelectedDate(worker[5])
        self.mail = QtWidgets.QLineEdit(worker[6])
        self.mail.setReadOnly(True)
        self.phone = QtWidgets.QLineEdit(worker[7])
        self.phone.setReadOnly(True)
        self.seriesPassport = QtWidgets.QLineEdit(worker[9])
        self.seriesPassport.setReadOnly(True)
        self.numberPassport = QtWidgets.QLineEdit(worker[10])
        self.numberPassport.setReadOnly(True)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.addWidget(self.label, 0, 0)
        self.gridLayout.addWidget(self.label1, 1, 0)
        self.gridLayout.addWidget(self.label2, 2, 0)
        self.gridLayout.addWidget(self.label3, 3, 0)
        self.gridLayout.addWidget(self.label4, 4, 0)
        self.gridLayout.addWidget(self.label5, 5, 0)
        self.gridLayout.addWidget(self.label6, 6, 0)
        self.gridLayout.addWidget(self.label7, 7, 0)
        self.gridLayout.addWidget(self.label8, 8, 0)
        self.gridLayout.addWidget(self.surname, 0, 1)
        self.gridLayout.addWidget(self.name, 1, 1)
        self.gridLayout.addWidget(self.patronymic, 2, 1)
        self.gridLayout.addWidget(self.gender, 3, 1)
        self.gridLayout.addWidget(self.dateBirthday, 4, 1)
        self.gridLayout.addWidget(self.mail, 5, 1)
        self.gridLayout.addWidget(self.phone, 6, 1)
        self.gridLayout.addWidget(self.seriesPassport, 7, 1)
        self.gridLayout.addWidget(self.numberPassport, 8, 1)
        self.widgetWithdata = QtWidgets.QWidget()
        self.widgetWithdata.setLayout(self.gridLayout)
        self.deleteButton = QtWidgets.QPushButton('Удалить')
        self.exitButton = QtWidgets.QPushButton('Выйти')
        self.exitButton.clicked.connect(self.exitButtonClicked)
        self.hBoxLayout = QtWidgets.QHBoxLayout()
        self.hBoxLayout.addWidget(self.exitButton)
        self.widgetWithButtons = QtWidgets.QWidget()
        self.widgetWithButtons.setLayout(self.hBoxLayout)
        self.vBoxLayout = QtWidgets.QVBoxLayout()
        self.vBoxLayout.addWidget(self.widgetWithdata)
        self.vBoxLayout.addWidget(self.widgetWithButtons)
        self.setLayout(self.vBoxLayout)

    def updateData(self):
        pass

    def exitButtonClicked(self):
        messageBox = QtWidgets.QMessageBox()
        messageBox.setWindowTitle('Предупреждение?')
        messageBox.addButton('Да', 5)
        messageBox.addButton('Нет', 6)
        messageBox.setText('Выйти из личного кабинета?')
        reply = messageBox.exec()
        if reply == 0:
            self.parent().parent().parent().idWorker = 0

            self.parent().parent().parent().setAuthorizationWidget()