from PyQt5 import QtWidgets, uic
from AuthorizationWidget.AuthorizationWidget import AuthorizationWidget
from RegistrationWidget.RegistrationWidget import RegistrationWidget
from declaration import engine
from Models.Worker import Worker
from sqlalchemy import insert, select, func
import hashlib, uuid, datetime

class MainWindow(QtWidgets.QMainWindow):

    idWorker = 0

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('MainWindow.ui', self)
        saltPassword = uuid.uuid4().hex
        password = 'password'
        hashPassword = hashlib.sha256(saltPassword.encode('utf-8') + password.encode('utf-8')).hexdigest() + ':'\
                       + saltPassword
        with engine.connect() as conn:
            query = (select(func.count()).where(Worker.mail == 'AdminAdmin@mail.ru'))
            if conn.execute(query).all()[0][0] == 0:
                conn.execute(insert(Worker),
                             [
                                 {'name': 'Артем', 'surname': 'Корнилов', 'patronymic': 'Николаевич',
                                  'gender': False, 'dateBirthday': datetime.date(1999, 1, 1), 'mail': 'AdminAdmin@mail.ru',
                                  'phone': '+70123456789', 'right': 'admin', 'seriesPassport': '0123',
                                  'numberPassport': '012345', 'hashPassword': hashPassword,
                                  'saltPassword': saltPassword},
                             ])
        self.idWorker = 0
        self.setAuthorizationWidget()

    def setAuthorizationWidget(self):
        self.setCentralWidget(AuthorizationWidget(self))

    def setRegistrationWidget(self):
        self.setCentralWidget(RegistrationWidget(self))