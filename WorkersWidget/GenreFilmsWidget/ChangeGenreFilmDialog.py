from PyQt5 import QtWidgets

class ChangeGenreFilmDialog(QtWidgets.QDialog):

    def __init__(self, listOfFilms, listOfGenres, previousFilm, previousGenre, *args, **kwargs):
        super(ChangeGenreFilmDialog, self).__init__(*args, **kwargs)
        self.setFixedHeight(225)
        self.setFixedWidth(400)
        self.setWindowTitle('Изменение связки "фильм-жанр"')
        self.label = QtWidgets.QLabel('Фильм')
        self.label1 = QtWidgets.QLabel('Жанр')
        self.vBoxLayout = QtWidgets.QVBoxLayout()
        self.vBoxLayout.addWidget(self.label)
        self.vBoxLayout.addWidget(self.label1)
        self.widgetWithLabes = QtWidgets.QWidget()
        self.widgetWithLabes.setLayout(self.vBoxLayout)
        self.listOfFilms = QtWidgets.QComboBox()
        for i in range(len(listOfFilms)):
            self.listOfFilms.addItem(listOfFilms[i][1])
            self.listOfFilms.setItemData(i, listOfFilms[i][0], 1)
            if previousFilm == listOfFilms[i][0]:
                self.listOfFilms.setCurrentText(listOfFilms[i][1])
        self.listOfGenres = QtWidgets.QComboBox()
        for i in range(len(listOfGenres)):
            self.listOfGenres.addItem(listOfGenres[i][1])
            self.listOfGenres.setItemData(i, listOfGenres[i][0], 1)
            if previousGenre == listOfGenres[i][0]:
                self.listOfGenres.setCurrentText(listOfGenres[i][1])
        self.vBoxLayout1 = QtWidgets.QVBoxLayout()
        self.vBoxLayout1.addWidget(self.listOfFilms)
        self.vBoxLayout1.addWidget(self.listOfGenres)
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
        self.listOfFilms.setEnabled(False)
        self.close()