import typing

import serial
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QProgressBar
from PyQt5 import QtCore

from pyqtgraph import PlotWidget


def rgb(color1, color2, value):
    r1, r2 = int(color1[1:3], 16) + 256, int(color2[1:3], 16) + 256
    g1, g2 = int(color1[3:5], 16) + 256, int(color2[3:5], 16) + 256
    b1, b2 = int(color1[5:7], 16) + 256, int(color2[5:7], 16) + 256
    n = value / 100
    r = str(hex(int(((r1 + r2) * n))))[3:]
    g = str(hex(int(((g1 + g2) * n))))[3:]
    b = str(hex(int(((b1 + b2) * n))))[3:]
    return '#' + r + g + b


class Window(QWidget):
    def __init__(self, *, width=800, height=600, resizable=False, title='NoTitle', pal=None):
        super(Window, self).__init__()

        self.resize(width, height)
        if resizable:
            self.setMaximumSize(width, height)
            self.setMinimumSize(width, height)

        self.setWindowTitle(title)

        if pal is None:
            pal = self.palette()
            pal.setColor(QPalette.Normal, QPalette.Window, QColor("#000000"))
            pal.setColor(QPalette.Inactive, QPalette.Window, QColor("#303030"))
        self.setPalette(pal)


class EntryBox(QLineEdit):
    def __init__(self, parent, *, x=0, y=0, font=['Comic Sans MS', 20], text='Text'):
        super().__init__(parent)

        self.move(x, y)
        self.setFont(QFont(*font))
        self.setPlaceholderText(text)


class Button(QPushButton):
    def __init__(self, name, parent, func: typing.Callable[[], None], *, x=0, y=0, font=['Comic Sans MS', 20]):
        super().__init__(name, parent)

        self.move(x, y)
        self.setFont(QFont(*font))
        self.clicked.connect(func)


class Plot(PlotWidget):
    def __init__(self, parent, geometry):
        super().__init__(parent)

        self.setGeometry(*geometry)


class Scale(QProgressBar):
    def __init__(self, parent, geometry, *, value=0, gradient=False, vertical=False, color1='#00ff00',
                 color2='#ff0000'):
        super().__init__(parent)

        self.color1 = color1
        self.color2 = color2
        self.setGeometry(*geometry)
        self.setValue(value)
        if gradient:
            self.setStyleSheet(
                "QProgressBar::chunk " + "{" + "background: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 {0}, stop: 1 {1});".format(
                    rgb(self.color1, self.color2, value), color1) + "}")
        if vertical:
            self.setOrientation(QtCore.Qt.Vertical)

    def gradient(self, value):
        self.setStyleSheet(
            "QProgressBar::chunk " + "{" + "background: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 {0}, stop: 1 {1});".format(
                rgb(self.color1, self.color2, value), self.color1) + "}")

    def update_self(self, value):
        self.setValue(value)
        self.gradient(value)


class Port:
    """
    it's a cool thing
    """
    def __init__(self, port, speed):
        self.port = serial.Serial(port, 115200)


if __name__ == '__main__':
    def connect():
        port = serial.Serial(box.text(), 115200)
        word = ''
        while True:
            sym = port.read()
            if sym == b'\r':
                pass
            if sym == b'\n':
                word = ''
            else:
                word += str(sym)[2:3]

    def close_port(port):
        port.close()


    app = QApplication([])
    win = Window(resizable=True, title="LemonLold's application")

    plot = Plot(win, [5, 5, 540, 350])
    p1 = plot.plot(pen='r')
    p2 = plot.plot(pen='g')
    p3 = plot.plot(pen='b')

    box = EntryBox(win, x=5, y=545, text='Enter port:')
    btn = Button('Connect', win, connect, x=290, y=545)

    temp = Scale(win, [550, 5, 70, 350], gradient=True, vertical=True, value=50)
    #temp.update_self(100)

    win.show()
    app.exec_()
