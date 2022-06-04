from PyQt5 import QtWidgets

class ChangeHallDialog(QtWidgets.QDialog):

    def __init__(self, listOfCinemas, listOfTypesOfHall,
                 previousNumber, previousCinema, previousTypeOfHall,  *args, **kwargs):
        super(ChangeHallDialog, self).__init__(*args, **kwargs)
        self.setFixedHeight(225)
        self.setFixedWidth(400)
        self.setWindowTitle('Изменение зала')
        self.label = QtWidgets.QLabel('Номер зала')
        self.label1 = QtWidgets.QLabel('Кинотеатр')
        self.label2 = QtWidgets.QLabel('Тип зала')
        self.vBoxLayout = QtWidgets.QVBoxLayout()
        self.vBoxLayout.addWidget(self.label)
        self.vBoxLayout.addWidget(self.label1)
        self.vBoxLayout.addWidget(self.label2)
        self.widgetWithLabes = QtWidgets.QWidget()
        self.widgetWithLabes.setLayout(self.vBoxLayout)
        self.lineEdit = QtWidgets.QLineEdit(previousNumber)
        self.listOfCinemas = QtWidgets.QComboBox()
        for i in range(len(listOfCinemas)):
            self.listOfCinemas.addItem(listOfCinemas[i][1])
            self.listOfCinemas.setItemData(i, listOfCinemas[i][0], 1)
            if previousCinema == listOfCinemas[i][0]:
                self.listOfCinemas.setCurrentText(listOfCinemas[i][1])
        self.listOfTypesOfHall = QtWidgets.QComboBox()
        for i in range(len(listOfTypesOfHall)):
            self.listOfTypesOfHall.addItem(listOfTypesOfHall[i][1])
            self.listOfTypesOfHall.setItemData(i, listOfTypesOfHall[i][0], 1)
            if previousTypeOfHall == listOfTypesOfHall[i][0]:
                self.listOfTypesOfHall.setCurrentText(listOfTypesOfHall[i][1])
        self.vBoxLayout1 = QtWidgets.QVBoxLayout()
        self.vBoxLayout1.addWidget(self.lineEdit)
        self.vBoxLayout1.addWidget(self.listOfCinemas)
        self.vBoxLayout1.addWidget(self.listOfTypesOfHall)
        self.widgetWithData = QtWidgets.QWidget()
        self.widgetWithData.setLayout(self.vBoxLayout1)
        self.hBoxLayout = QtWidgets.QHBoxLayout()
        self.hBoxLayout.addWidget(self.widgetWithLabes)
        self.hBoxLayout.addWidget(self.widgetWithData)
        self.widgetWithTypesOfHall = QtWidgets.QWidget()
        self.widgetWithTypesOfHall.setLayout(self.hBoxLayout)
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
        self.vBoxLayout2.addWidget(self.widgetWithTypesOfHall)
        self.vBoxLayout2.addWidget(self.widgetWithButtons)
        self.setLayout(self.vBoxLayout2)

    def addButtonClicked(self):
        self.lineEdit.setEnabled(False)
        self.close()