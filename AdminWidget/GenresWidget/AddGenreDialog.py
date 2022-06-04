from PyQt5 import QtWidgets

class AddGenreDialog(QtWidgets.QDialog):

    def __init__(self, *args, **kwargs):
        super(AddGenreDialog, self).__init__(*args, **kwargs)
        self.setFixedHeight(180)
        self.setFixedWidth(360)
        self.setWindowTitle('Добавление жанра')
        self.label = QtWidgets.QLabel('Наименование')
        self.lineEdit = QtWidgets.QLineEdit()
        self.hBoxtalLayout1 = QtWidgets.QHBoxLayout()
        self.hBoxtalLayout1.addWidget(self.label)
        self.hBoxtalLayout1.addWidget(self.lineEdit)
        self.widgetWithGenre = QtWidgets.QWidget()
        self.widgetWithGenre.setLayout(self.hBoxtalLayout1)
        self.hBoxtalLayout2 = QtWidgets.QHBoxLayout()
        self.addButton = QtWidgets.QPushButton('Добавить')
        self.addButton.clicked.connect(self.addButtonClicked)
        self.cancelButton = QtWidgets.QPushButton('Отменить')
        self.cancelButton.clicked.connect(self.close)
        self.hBoxtalLayout2.addWidget(self.addButton)
        self.hBoxtalLayout2.addWidget(self.cancelButton)
        self.widgetWithButtons = QtWidgets.QWidget()
        self.widgetWithButtons.setLayout(self.hBoxtalLayout2)
        self.vBoxlayout = QtWidgets.QVBoxLayout()
        self.vBoxlayout.addWidget(self.widgetWithGenre)
        self.vBoxlayout.addWidget(self.widgetWithButtons)
        self.setLayout(self.vBoxlayout)

    def addButtonClicked(self):
        self.lineEdit.setEnabled(False)
        self.close()