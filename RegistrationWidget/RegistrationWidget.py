from PyQt5 import QtWidgets, QtCore, Qt
from declaration import engine
from Models.Worker import Worker
from sqlalchemy import insert, select, func
from datetime import datetime
import hashlib, uuid

class RegistrationWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(RegistrationWidget, self).__init__(*args, **kwargs)
        self.label = QtWidgets.QLabel('Фамилия')
        self.label1 = QtWidgets.QLabel('Имя')
        self.label2 = QtWidgets.QLabel('Отчество')
        self.label3 = QtWidgets.QLabel('Пол')
        self.label4 = QtWidgets.QLabel('Дата рождения')
        self.label5 = QtWidgets.QLabel('Почта')
        self.label6 = QtWidgets.QLabel('Телефон')
        self.label7 = QtWidgets.QLabel('Серия паспорта')
        self.label8 = QtWidgets.QLabel('Номер паспорта')
        self.label9 = QtWidgets.QLabel('Пароль')
        self.label10 = QtWidgets.QLabel('Повтор пароля')
        self.surname = QtWidgets.QLineEdit()
        self.surname.setValidator(Qt.QRegExpValidator(QtCore.QRegExp('[А-ЩЭ-ЯЁ][а-яё]{29}')))
        self.name = QtWidgets.QLineEdit()
        self.name.setValidator(Qt.QRegExpValidator(QtCore.QRegExp('[А-ЩЭ-ЯЁ][а-яё]{19}')))
        self.patronymic = QtWidgets.QLineEdit()
        self.patronymic.setValidator(Qt.QRegExpValidator(QtCore.QRegExp('[А-ЩЭ-ЯЁ][а-яё]{29}')))
        self.gender = QtWidgets.QComboBox()
        self.gender.addItem('Мужской')
        self.gender.addItem('Женский')
        self.dateBirthday = QtWidgets.QCalendarWidget()
        self.dateBirthday.setMinimumDate(QtCore.QDate(1990, 1, 1))
        self.dateBirthday.setMaximumDate(datetime.now().date())
        self.dateBirthday.setSelectionMode(self.dateBirthday.SelectionMode.SingleSelection)
        self.mail = QtWidgets.QLineEdit()
        self.mail.setValidator(Qt.QRegExpValidator(QtCore.QRegExp('[a-zA-Z@.]{30}')))
        self.phone = QtWidgets.QLineEdit()
        self.phone.setValidator(Qt.QRegExpValidator(QtCore.QRegExp( '[+][0-9]{11}')))
        self.seriesPassport = QtWidgets.QLineEdit()
        self.seriesPassport.setValidator(Qt.QRegExpValidator(QtCore.QRegExp('[0-9]{4}')))
        self.numberPassport = QtWidgets.QLineEdit()
        self.numberPassport.setValidator(Qt.QRegExpValidator(QtCore.QRegExp('[0-9]{6}')))
        self.password = QtWidgets.QLineEdit()
        self.password.setEchoMode(self.password.EchoMode.Password)
        self.repeatPassword = QtWidgets.QLineEdit()
        self.repeatPassword.setEchoMode(self.repeatPassword.EchoMode.Password)
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
        self.gridLayout.addWidget(self.label9, 9, 0)
        self.gridLayout.addWidget(self.label10, 10, 0)
        self.gridLayout.addWidget(self.surname, 0, 1)
        self.gridLayout.addWidget(self.name, 1, 1)
        self.gridLayout.addWidget(self.patronymic, 2, 1)
        self.gridLayout.addWidget(self.gender, 3, 1)
        self.gridLayout.addWidget(self.dateBirthday, 4, 1)
        self.gridLayout.addWidget(self.mail, 5, 1)
        self.gridLayout.addWidget(self.phone, 6, 1)
        self.gridLayout.addWidget(self.seriesPassport, 7, 1)
        self.gridLayout.addWidget(self.numberPassport, 8, 1)
        self.gridLayout.addWidget(self.password, 9, 1)
        self.gridLayout.addWidget(self.repeatPassword, 10, 1)
        self.widgetWithdata = QtWidgets.QWidget()
        self.widgetWithdata.setLayout(self.gridLayout)
        self.registrateButton = QtWidgets.QPushButton('Зарегистрироваться')
        self.authorizationButton = QtWidgets.QPushButton('Авторизация')
        self.registrateButton.clicked.connect(self.registrateButtonClicked)
        self.authorizationButton.clicked.connect(self.authorizationButtonClicked)
        self.hBoxLayout = QtWidgets.QHBoxLayout()
        self.hBoxLayout.addWidget(self.registrateButton)
        self.hBoxLayout.addWidget(self.authorizationButton)
        self.widgetWithButtons = QtWidgets.QWidget()
        self.widgetWithButtons.setLayout(self.hBoxLayout)
        self.vBoxLayout = QtWidgets.QVBoxLayout()
        self.vBoxLayout.addWidget(self.widgetWithdata)
        self.vBoxLayout.addWidget(self.widgetWithButtons)
        self.groupBox = QtWidgets.QGroupBox('Регистрация')
        self.groupBox.setLayout(self.vBoxLayout)
        self.gridLayout2 = QtWidgets.QGridLayout()
        self.gridLayout2.addWidget(self.groupBox)
        self.setLayout(self.gridLayout2)

    def registrateButtonClicked(self):
        if self.surname.text() == '':
            messageBox = QtWidgets.QMessageBox()
            messageBox.setWindowTitle('Ошибка')
            messageBox.addButton('Ок', 5)
            messageBox.setText('Не была введена фамилия!')
            messageBox.exec()
        elif self.name.text() == '':
            messageBox = QtWidgets.QMessageBox()
            messageBox.setWindowTitle('Ошибка')
            messageBox.addButton('Ок', 5)
            messageBox.setText('Не было введено имя!')
            messageBox.exec()
        elif len(self.mail.text()) == '':
            print(self.dateBirthday.selectedDate())
            messageBox = QtWidgets.QMessageBox()
            messageBox.setWindowTitle('Ошибка')
            messageBox.addButton('Ок', 5)
            messageBox.setText('Не была ведена почта!')
            messageBox.exec()
        elif len(self.phone.text()) != 12:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setWindowTitle('Ошибка')
            messageBox.addButton('Ок', 5)
            messageBox.setText('Номер телефона должен состоять символа из \'+\' и 11 цифр!')
            messageBox.exec()
        elif len(self.seriesPassport.text()) != 4:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setWindowTitle('Ошибка')
            messageBox.addButton('Ок', 5)
            messageBox.setText('Серия паспорта должна состоять из 4 цифр!')
            messageBox.exec()
        elif len(self.numberPassport.text()) != 6:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setWindowTitle('Ошибка')
            messageBox.addButton('Ок', 5)
            messageBox.setText('Номер паспорта должен состоять из 6 цифр!')
            messageBox.exec()
        elif len(self.password.text()) < 8:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setWindowTitle('Ошибка')
            messageBox.addButton('Ок', 5)
            messageBox.setText('Длина пароля должна быть не меньше 8!')
            messageBox.exec()
        elif self.password.text() != self.repeatPassword.text():
            messageBox = QtWidgets.QMessageBox()
            messageBox.setWindowTitle('Ошибка')
            messageBox.addButton('Ок', 5)
            messageBox.setText('Пароли не совпадают!')
            messageBox.exec()
        else:
            with engine.connect() as conn:
                if conn.execute(select(func.count()).where(Worker.mail == self.mail.text())).all()[0][0] != 0:
                    messageBox = QtWidgets.QMessageBox()
                    messageBox.setWindowTitle('Ошибка')
                    messageBox.addButton('Ок', 5)
                    messageBox.setText('Аккаунт с такой почтой уже существует!')
                    messageBox.exec()
                    conn.close()
                else:
                    saltPassword = uuid.uuid4().hex
                    conn.execute(
                        insert(Worker),
                        [
                            {'name': self.name.text(),
                            'surname': self.surname.text(),
                            'patronymic': self.patronymic.text(),
                            'gender': False if self.gender.currentIndex() == 0 else True,
                            'dateBirthday': self.dateBirthday.selectedDate().toString('dd-MM-yyyy'),
                            'mail': self.mail.text(),
                            'phone': self.phone.text(),
                            'right': 'lockedWorker',
                            'seriesPassport': self.seriesPassport.text(),
                            'numberPassport': self.numberPassport.text(),
                            'hashPassword': hashlib.sha256(saltPassword.encode('utf-8')
                                                            + self.password.text().encode('utf-8'))
                                                 .hexdigest() + ':' + saltPassword,
                            'saltPassword': saltPassword},
                        ]
                    )
                    conn.close()
                    messageBox = QtWidgets.QMessageBox()
                    messageBox.setWindowTitle('Предупреждение')
                    messageBox.addButton('Ок', 5)
                    messageBox.setText('Регистрация прошла успешно!')
                    messageBox.exec()
                    self.parent().setAuthorizationWidget()

    def authorizationButtonClicked(self):
        self.parent().setAuthorizationWidget()