import time

from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtWidgets import QApplication, QLineEdit, QPushButton, QWidget, QLabel, QProgressBar
from PyQt5 import QtCore
from pyqtgraph import PlotWidget
import serial


def rgb(value):
    r = 255*value//100
    g = 255*(100-value)//100
    if g == 0:
        return '#ff0000'
    elif r == 0:
        return '#00ff00'
    return '#'+str(hex(r))[2:]+str(hex(g))[2:]+'00'


class Window(QWidget):
    def __init__(self):
        super().__init__()

        w, h = 800, 600
        self.resize(w, h)
        self.setMaximumSize(w, h)
        self.setMinimumSize(w, h)

        self.setWindowTitle('Lemonade')

        pal = self.palette()
        pal.setColor(QPalette.Normal, QPalette.Window, QColor("#000000"))
        pal.setColor(QPalette.Inactive, QPalette.Window, QColor("#404040"))
        self.setPalette(pal)


class Scale(QProgressBar):
    def __init__(self, parent, value):
        super().__init__(parent)

        self.setGeometry(550, 5, 70, 350)
        self.setValue(value)
        self.setStyleSheet("QProgressBar::chunk "+"{"+"background: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 {0}, stop: 1 #00ff00);".format(rgb(value))+"}")
        self.setOrientation(QtCore.Qt.Vertical)


class Plot(PlotWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.setYRange(0, 160)
        self.setGeometry(5, 5, 540, 350)


class Button(QPushButton):
    def __init__(self, name, parent):
        super().__init__(name, parent)

        self.move(290, 545)
        self.setFont(QFont('Comic Sans MS', 20))
        self.clicked.connect(connecting)


class EntryBox(QLineEdit):
    def __init__(self, parent):
        super().__init__(parent)

        self.move(5, 545)
        self.setFont(QFont('Comic Sans MS', 20))
        self.setText('Enter port name:')


def update(points_lst, new_point, graphics, temp, value):
    for i in range(len(graphics)):
        points_lst[i].append(new_point[i])
        if len(points_lst[i]) > 15:
            points_lst[i] = points_lst[i][-15:]
        graphics[i].setData(points_lst[i])
    temp.setValue(value)
    temp.setStyleSheet("QProgressBar::chunk "+"{"+"background: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 {0}, stop: 1 #00ff00);".format(rgb(value))+"}")
    QApplication.processEvents()
    return points_lst


if __name__ == '__main__':

    def connecting():
        port = open('data.txt', 'r')
        data = ''
        values = [[], [], []]
        for line in port:
            data = [float(i) for i in str(line).split()]
            values = update(values, data[:3], [p1, p2, p3], temp, int(data[3]))
            time.sleep(1)
        '''
        port = serial.Serial(box.text(), 38400)
        data = ''
        values = [[], [], []]
        while True:
            sym = port.read(1)
            print(sym)
            if sym == b'\r':
                values = update(values, [float(i) for i in data.split()], [p1, p2, p3])
            if sym == b'\n':
                data = ''
            else:
                data += str(sym)[2:3]
        '''


    app = QApplication([])
    win = Window()
    plot1 = Plot(win)
    p1 = plot1.plot(pen='r')
    p2 = plot1.plot(pen='g')
    p3 = plot1.plot(pen='b')
    btn = Button('Connect', win)
    box = EntryBox(win)
    lbl = QLabel(win)
    lbl.setText('red - x; green = y; blue = z')
    lbl.setFont(QFont('Comic Sans MS', 20))
    lbl.move(405, 540)
    temp = Scale(win, 0)
    win.show()
    app.exec_()