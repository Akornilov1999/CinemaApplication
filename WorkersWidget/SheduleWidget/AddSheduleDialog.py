from PyQt5 import QtWidgets, QtCore
from datetime import date

class AddSheduleDialog(QtWidgets.QDialog):

    def __init__(self, listOfFilms, listOfHalls, *args, **kwargs):
        super(AddSheduleDialog, self).__init__(*args, **kwargs)
        self.setFixedHeight(500)
        self.setFixedWidth(400)
        self.setWindowTitle('Добавление расписания')
        self.label = QtWidgets.QLabel('Дата')
        self.label1 = QtWidgets.QLabel('Фильм')
        self.label2 = QtWidgets.QLabel('Зал')
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.addWidget(self.label, 0, 0)
        self.gridLayout.addWidget(self.label1, 1, 0)
        self.gridLayout.addWidget(self.label2, 2, 0)
        self.date = QtWidgets.QCalendarWidget()
        self.date.setMinimumDate(date.today())
        self.date.setMaximumDate(date.today().replace(date.today().year, date.today().month + 1, date.today().day))
        self.date.setSelectionMode(self.date.SelectionMode.SingleSelection)
        self.listOfFilms = QtWidgets.QComboBox()
        for i in range(len(listOfFilms)):
            self.listOfFilms.addItem(listOfFilms[i][1])
            self.listOfFilms.setItemData(i, listOfFilms[i][0], 1)
        self.listOfHalls = QtWidgets.QComboBox()
        for i in range(len(listOfHalls)):
            self.listOfHalls.addItem(listOfHalls[i][1])
            self.listOfHalls.setItemData(i, listOfHalls[i][0], 1)
        self.gridLayout.addWidget(self.date, 0, 1)
        self.gridLayout.addWidget(self.listOfFilms, 1, 1)
        self.gridLayout.addWidget(self.listOfHalls, 2, 1)
        self.widgetWithData = QtWidgets.QWidget()
        self.widgetWithData.setLayout(self.gridLayout)
        self.widgetWithShedule = QtWidgets.QWidget()
        self.widgetWithShedule.setLayout(self.gridLayout)
        self.addButton = QtWidgets.QPushButton('Добавить')
        self.addButton.clicked.connect(self.addButtonClicked)
        self.cancelButton = QtWidgets.QPushButton('Отменить')
        self.cancelButton.clicked.connect(self.close)
        self.hBoxLayout1 = QtWidgets.QHBoxLayout()
        self.hBoxLayout1.addWidget(self.addButton)
        self.hBoxLayout1.addWidget(self.cancelButton)
        self.widgetWithButtons = QtWidgets.QWidget()
        self.widgetWithButtons.setLayout(self.hBoxLayout1)
        self.vBoxLayout2 = QtWidgets.QVBoxLayout()
        self.vBoxLayout2.addWidget(self.widgetWithShedule)
        self.vBoxLayout2.addWidget(self.widgetWithButtons)
        self.setLayout(self.vBoxLayout2)

    def addButtonClicked(self):
        self.listOfFilms.setEnabled(False)
        self.close()