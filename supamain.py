import sys

from PyQt5 import QtWidgets, uic


class SecondWindow(QtWidgets.QWidget):
    def __init__(self, ui_sample: str, *args, **kwargs):
        super(SecondWindow, self).__init__(*args, **kwargs)

        # Загрузите страницу интерфейса
        uic.loadUi(ui_sample, self)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, ui_sample: str, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Загрузите страницу интерфейса
        uic.loadUi(ui_sample, self)


def scenario1():
    print('scenario1 success')
    portWindow.show()
    inputWindow.close()


def scenario2():
    print('scenario2 success')
    fileWindow.show()
    inputWindow.close()


app = QtWidgets.QApplication(sys.argv)
inputWindow = SecondWindow("inputWindow.ui")
fileWindow = MainWindow("fileOutputWindow.ui")
portWindow = MainWindow("portOutputWindow.ui")
logWindow = SecondWindow("logWindow.ui")
inputWindow.portConnectButton.clicked.connect(scenario1)
inputWindow.fileReadButton.clicked.connect(scenario2)
inputWindow.show()
sys.exit(app.exec_())
