import sys
from PyQt5 import QtWidgets, QtCore, uic
from MainWindow import MainWindow
import AdminWidget.AdminWidget
from declaration import engine
from sqlalchemy import select, func

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

