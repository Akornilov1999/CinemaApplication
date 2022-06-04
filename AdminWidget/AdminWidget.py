from PyQt5 import QtWidgets
from AdminWidget.CitiesWidget.CitiesWidget import CitiesWidget
from AdminWidget.CinemasWidget.CinemasWidget import CinemasWidget
from AdminWidget.TypesOfHallWidget.TypesOfHallWidget import TypesOfHallWidget
from AdminWidget.HallsWidget.HallsWidget import HallsWidget
from AdminWidget.CompaniesWidget.CompanyWidget import CompaniesWidget
from AdminWidget.GenresWidget.GenresWidget import GenresWidget
from AdminWidget.ListOfWorkersWidget.ListOfWorkersWidget import ListOfWorkersWidget
from PersonalAccountWidget.PersonalAccountWidget import PersonalAccountWidget

class AdminWidget(QtWidgets.QTabWidget):

    def __init__(self, *args, **kwargs):
        super(AdminWidget, self).__init__(*args, **kwargs)
        self.addTab(CitiesWidget(self), 'Города')
        self.addTab(CinemasWidget(self), 'Кинотеатры')
        self.addTab(TypesOfHallWidget(self), 'Типы залов')
        self.addTab(HallsWidget(self), 'Залы')
        self.addTab(GenresWidget(), 'Жанры')
        self.addTab(CompaniesWidget(self), 'Киностудии')
        self.addTab(ListOfWorkersWidget(self), 'Сотрудники')
        self.addTab(PersonalAccountWidget(self.parent()), 'Личный кабинет')
        self.currentChanged.connect(self.updateData)

    def updateData(self, index):
        self.widget(index).updateData()