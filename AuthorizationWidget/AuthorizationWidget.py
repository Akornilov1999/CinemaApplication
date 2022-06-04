from PyQt5 import QtWidgets, QtCore, Qt
from declaration import engine
from Models.Worker import Worker
from sqlalchemy import insert, select, func
from AdminWidget.AdminWidget import AdminWidget
from WorkersWidget.WorkersWidget import WorkersWidget
import hashlib, uuid

class AuthorizationWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(AuthorizationWidget, self).__init__(*args, **kwargs)
        self.label = QtWidgets.QLabel('Почта')
        self.label1 = QtWidgets.QLabel('Пароль')
        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit1 = QtWidgets.QLineEdit()
        self.lineEdit1.setEchoMode(self.lineEdit.EchoMode.Password)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.addWidget(self.label, 0, 0)
        self.gridLayout.addWidget(self.label1, 1, 0)
        self.gridLayout.addWidget(self.lineEdit, 0, 1)
        self.gridLayout.addWidget(self.lineEdit1, 1, 1)
        self.widgetWithData = QtWidgets.QWidget()
        self.widgetWithData.setLayout(self.gridLayout)
        self.widgetWithData.setLayout(self.gridLayout)
        self.authorizeButton = QtWidgets.QPushButton('Войти')
        self.authorizeButton.clicked.connect(self.authorizedButtonClicked)
        self.registrationButton = QtWidgets.QPushButton('Регистрация')
        self.registrationButton.clicked.connect(self.registrationButtonClicked)
        self.hBoxLayout = QtWidgets.QHBoxLayout()
        self.hBoxLayout.addWidget(self.authorizeButton)
        self.hBoxLayout.addWidget(self.registrationButton)
        self.widgetWithButtons = QtWidgets.QWidget()
        self.widgetWithButtons.setLayout(self.hBoxLayout)
        self.vBoxLayout = QtWidgets.QVBoxLayout()
        self.vBoxLayout.addWidget(self.widgetWithData)
        self.vBoxLayout.addWidget(self.widgetWithButtons)
        self.groupBox = QtWidgets.QGroupBox('Авторизация')
        self.groupBox.setLayout(self.vBoxLayout)
        self.gridLayout2 = QtWidgets.QGridLayout()
        self.gridLayout2.addItem(Qt.QSpacerItem(0, 0, vPolicy=Qt.QSizePolicy.Expanding,
                                                hPolicy=Qt.QSizePolicy.Minimum), 0, 1)
        self.gridLayout2.addItem(Qt.QSpacerItem(0, 0, hPolicy=Qt.QSizePolicy.Expanding,
                                                vPolicy=Qt.QSizePolicy.Minimum), 1, 0)
        self.gridLayout2.addWidget(self.groupBox, 1, 1)
        self.gridLayout2.addItem(Qt.QSpacerItem(0, 0, hPolicy=Qt.QSizePolicy.Expanding, vPolicy=Qt.QSizePolicy.Minimum), 1, 2)
        self.gridLayout2.addItem(Qt.QSpacerItem(0, 0, vPolicy=Qt.QSizePolicy.Expanding, hPolicy=Qt.QSizePolicy.Minimum), 2, 1)
        self.setLayout(self.gridLayout2)

    def updateData(self):
        pass

    def authorizedButtonClicked(self):
        if self.lineEdit.text() == '':
            messageBox = QtWidgets.QMessageBox()
            messageBox.setWindowTitle('Ошибка')
            messageBox.addButton('Ок', 5)
            messageBox.setText('Не была введена почта!')
            messageBox.exec()
        elif self.label1.text() == '':
            messageBox = QtWidgets.QMessageBox()
            messageBox.setWindowTitle('Ошибка')
            messageBox.addButton('Ок', 5)
            messageBox.setText('Не был введен пароль!')
            messageBox.exec()
        else:
            with engine.connect() as conn:
                query = (select(Worker).where(Worker.mail == self.lineEdit.text()))
                if len(conn.execute(query).all()) != 1:
                    messageBox = QtWidgets.QMessageBox()
                    messageBox.setWindowTitle('Ошибка')
                    messageBox.addButton('Ок', 5)
                    messageBox.setText('Введены неверные почта или пароль!')
                    messageBox.exec()
                elif conn.execute((query)).all()[0][11] != hashlib.sha256(
                        conn.execute((query)).all()[0][12].encode('utf-8')
                        + self.lineEdit1.text().encode('utf-8'))\
                                       .hexdigest() + ':' + conn.execute((query)).all()[0][12]:
                    messageBox = QtWidgets.QMessageBox()
                    messageBox.setWindowTitle('Ошибка')
                    messageBox.addButton('Ок', 5)
                    messageBox.setText('Введены неверные почта или пароль!')
                    messageBox.exec()
                elif conn.execute((query)).all()[0][8] == 'admin':
                    self.parent().idWorker = conn.execute((query)).all()[0][0]
                    self.parent().setCentralWidget(AdminWidget(self.parent()))
                elif conn.execute((query)).all()[0][8] == 'lockedWorker':
                    self.parent().idWorker = conn.execute((query)).all()[0][0]
                    messageBox = QtWidgets.QMessageBox()
                    messageBox.setWindowTitle('Предупреждение')
                    messageBox.addButton('Ок', 5)
                    messageBox.setText('Подождите, пока администратор предоставит Вам доступ!')
                    messageBox.exec()
                elif conn.execute((query)).all()[0][8] == 'unlockedWorker':
                    self.parent().idWorker = conn.execute((query)).all()[0][0]
                    self.parent().setCentralWidget(WorkersWidget(self.parent()))

    def registrationButtonClicked(self):
        self.parent().setRegistrationWidget()