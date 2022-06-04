from PyQt5 import QtWidgets

class RenameGenreDialog(QtWidgets.QDialog):

    def __init__(self, name,*args, **kwargs):
        super(RenameGenreDialog, self).__init__(*args, **kwargs)
        self.setFixedHeight(180)
        self.setFixedWidth(360)
        self.setWindowTitle('Переименование жанра')
        self.label = QtWidgets.QLabel('Наименование')
        self.lineEdit = QtWidgets.QLineEdit(name)
        self.hBoxtalLayout1 = QtWidgets.QHBoxLayout()
        self.hBoxtalLayout1.addWidget(self.label)
        self.hBoxtalLayout1.addWidget(self.lineEdit)
        self.widgetWithGenre = QtWidgets.QWidget()
        self.widgetWithGenre.setLayout(self.hBoxtalLayout1)
        self.hBoxtalLayout2 = QtWidgets.QHBoxLayout()
        self.addButton = QtWidgets.QPushButton('Переименовать')
        self.addButton.clicked.connect(self.renameButtonClicked)
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

    def renameButtonClicked(self):
        self.lineEdit.setEnabled(False)
        self.close()