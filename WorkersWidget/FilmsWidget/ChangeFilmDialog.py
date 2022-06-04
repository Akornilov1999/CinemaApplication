from PyQt5 import QtWidgets, QtCore
from datetime import time

class ChangeFilmDialog(QtWidgets.QDialog):

    def __init__(self, listOfCompanies, previousName, previousDuration,
                 previousAgeLimit, previousCompany, *args, **kwargs):
        super(ChangeFilmDialog, self).__init__(*args, **kwargs)
        self.setFixedHeight(225)
        self.setFixedWidth(400)
        self.setWindowTitle('Изменение фильма')
        self.label = QtWidgets.QLabel('Название')
        self.label1 = QtWidgets.QLabel('Продолжительность')
        self.label2 = QtWidgets.QLabel('Возрастное ограничение')
        self.label3 = QtWidgets.QLabel('Киностудия')
        self.vBoxLayout = QtWidgets.QVBoxLayout()
        self.vBoxLayout.addWidget(self.label)
        self.vBoxLayout.addWidget(self.label1)
        self.vBoxLayout.addWidget(self.label2)
        self.vBoxLayout.addWidget(self.label3)
        self.widgetWithLabes = QtWidgets.QWidget()
        self.widgetWithLabes.setLayout(self.vBoxLayout)
        self.lineEdit = QtWidgets.QLineEdit(previousName)
        self.duration = QtWidgets.QTimeEdit()
        self.duration.setMinimumTime(time(1, 20, 0))
        self.duration.setMaximumTime(time(4, 30, 0))
        self.duration.setTime(time(int(previousDuration[0] + previousDuration[1]),
                                   int(previousDuration[3] + previousDuration[4]),
                                   int(previousDuration[6] + previousDuration[7])))
        self.ageLimit = QtWidgets.QSpinBox()
        self.ageLimit.setMinimum(0)
        self.ageLimit.setMaximum(18)
        self.ageLimit.setValue(int(previousAgeLimit))
        self.listOfCompanies = QtWidgets.QComboBox()
        for i in range(len(listOfCompanies)):
            self.listOfCompanies.addItem(listOfCompanies[i][1])
            self.listOfCompanies.setItemData(i, listOfCompanies[i][0], 1)
            if previousCompany == listOfCompanies[i][0]:
                self.listOfCompanies.setCurrentText(listOfCompanies[i][1])
        self.vBoxLayout1 = QtWidgets.QVBoxLayout()
        self.vBoxLayout1.addWidget(self.lineEdit)
        self.vBoxLayout1.addWidget(self.duration)
        self.vBoxLayout1.addWidget(self.ageLimit)
        self.vBoxLayout1.addWidget(self.listOfCompanies)
        self.widgetWithData = QtWidgets.QWidget()
        self.widgetWithData.setLayout(self.vBoxLayout1)
        self.hBoxLayout = QtWidgets.QHBoxLayout()
        self.hBoxLayout.addWidget(self.widgetWithLabes)
        self.hBoxLayout.addWidget(self.widgetWithData)
        self.widgetWithData = QtWidgets.QWidget()
        self.widgetWithData.setLayout(self.hBoxLayout)
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
        self.vBoxLayout2.addWidget(self.widgetWithData)
        self.vBoxLayout2.addWidget(self.widgetWithButtons)
        self.setLayout(self.vBoxLayout2)

    def addButtonClicked(self):
        self.lineEdit.setEnabled(False)
        self.close()