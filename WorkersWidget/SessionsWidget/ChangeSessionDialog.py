from PyQt5 import QtWidgets, QtCore
from datetime import datetime, date, time

class ChangeSessionDialog(QtWidgets.QDialog):

    def __init__(self, listOfShedule, previousTime, previousPrice, previousShedule, *args, **kwargs):
        super(ChangeSessionDialog, self).__init__(*args, **kwargs)
        self.setFixedHeight(225)
        self.setFixedWidth(750)
        self.setWindowTitle('Изменение сеанса')
        self.label = QtWidgets.QLabel('Время начала')
        self.label1 = QtWidgets.QLabel('Цена')
        self.label2 = QtWidgets.QLabel('Расписание')
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.addWidget(self.label, 0, 0)
        self.gridLayout.addWidget(self.label1, 1, 0)
        self.gridLayout.addWidget(self.label2, 2, 0)
        self.time = QtWidgets.QTimeEdit()
        self.time.setMinimumTime(time(10, 0, 0))
        self.time.setMaximumTime(time(22, 0, 0))
        self.time.setDisplayFormat('H:mm')
        self.time.setTime(previousTime)
        self.price = QtWidgets.QDoubleSpinBox()
        self.price.setMinimum(100)
        self.price.setMaximum(1000)
        self.price.setValue(previousPrice)
        self.listOfShedule = QtWidgets.QComboBox()
        for i in range(len(listOfShedule)):
            self.listOfShedule.addItem(listOfShedule[i][1])
            self.listOfShedule.setItemData(i, listOfShedule[i][0], 1)
            if previousShedule == listOfShedule[i][0]:
                self.listOfShedule.setCurrentIndex(i)
        self.gridLayout.addWidget(self.time, 0, 1)
        self.gridLayout.addWidget(self.price, 1, 1)
        self.gridLayout.addWidget(self.listOfShedule, 2, 1)
        self.widgetWithData = QtWidgets.QWidget()
        self.widgetWithData.setLayout(self.gridLayout)
        self.widgetWithSessions = QtWidgets.QWidget()
        self.widgetWithSessions.setLayout(self.gridLayout)
        self.addButton = QtWidgets.QPushButton('Изменить')
        self.addButton.clicked.connect(self.addButtonClicked)
        self.cancelButton = QtWidgets.QPushButton('Отменить')
        self.cancelButton.clicked.connect(self.close)
        self.hBoxLayout1 = QtWidgets.QHBoxLayout()
        self.hBoxLayout1.addWidget(self.addButton)
        self.hBoxLayout1.addWidget(self.cancelButton)
        self.widgetWithButtons = QtWidgets.QWidget()
        self.widgetWithButtons.setLayout(self.hBoxLayout1)
        self.vBoxLayout2 = QtWidgets.QVBoxLayout()
        self.vBoxLayout2.addWidget(self.widgetWithSessions)
        self.vBoxLayout2.addWidget(self.widgetWithButtons)
        self.setLayout(self.vBoxLayout2)

    def addButtonClicked(self):
        self.listOfShedule.setEnabled(False)
        self.close()