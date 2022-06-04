from PyQt5 import QtWidgets
from WorkersWidget.FilmsWidget.FilmsWidget import FilmsWidget
from WorkersWidget.GenreFilmsWidget.GenreFilmsWidget import GenreFilmsWidget
from WorkersWidget.SessionsWidget.SessionsWidget import SessionsWidget
from WorkersWidget.SheduleWidget.SheduleWidget import SheduleWidget
from PersonalAccountWidget.PersonalAccountWidget import PersonalAccountWidget

class WorkersWidget(QtWidgets.QTabWidget):

    def __init__(self, *args, **kwargs):
        super(WorkersWidget, self).__init__(*args, **kwargs)
        self.addTab(FilmsWidget(self), 'Фильмы')
        self.addTab(GenreFilmsWidget(self), 'Связка "фильм-жанр"')
        self.addTab(SessionsWidget(self), 'Сеансы')
        self.addTab(SheduleWidget(self), 'Расписание')
        self.addTab(PersonalAccountWidget(self.parent()), 'Личный кабинет')
        self.currentChanged.connect(self.updateData)

    def updateData(self, index):
        self.widget(index).updateData()