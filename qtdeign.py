import random
import sys
import time
import asyncio

import pyqtgraph.PlotData
import serial
from PyQt5 import QtWidgets, uic
from pyqtgraph.Qt import QtGui
import pyqtgraph as pg
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Загрузите страницу интерфейса
        uic.loadUi('titled.ui', self)

    """
    def catmode_on(self):
        oImage = QImage("cat-001.png")
        sImage = oImage.scaled(QSize(300, 200))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)
        self.catmode_btn.toggled.connect(main.catmode_off)
    """


"""def organize(data):
    n = data[0]
    data = data[1:]
    lst1 = []
    lst2 = [[] for i in range(n)]
    for i in range(n):
        lst1 += [i for _ in range(data[i])]
    for i, j in zip(lst1, data[n:]):
        lst2[i].append(j)
    print(lst2)
    if random.randint(1, 20) == 1:
        return ['a']
    else:
        return lst2


def update(new_values, sensors):
    for value, sensor in zip(new_values, sensors):
        if type(sensor) == list:
            for val, plot in zip(value, sensor):
                data = plot.getData()[1]
                data[:-1] = data[1:]
                data[-1] = val
                plot.setData(data)
        else:
            sensor.setValue(value[0])
        QtGui.QApplication.processEvents()




def mainloop():
    port = serial.Serial("COM5", 115200)
    data = ''
    while True:
        sym = port.read(1)
        if sym == b'\r':
            try:
                print(data)
                data = organize(list(map(int, data.split(' '))))
                update(data, [[plot1_x, plot1_y, plot1_z], [plot2_x, plot2_y, plot2_z],
                              main.temp1, main.temp2, main.press, main.height])
            except:
                pass
        if sym == b'\n':
            data = ''
        else:
            data += str(sym)[2:3]
    file = open('file', 'r')
    for line in file:
        data = [int(i) for i in line.split()]
        data = organize(data)
        update(data, [[plot1_x, plot1_y, plot1_z], [plot2_x, plot2_y, plot2_z],
                      main.temp1, main.temp2, main.press, main.height])
        """


"""def radioInput(port):
    data = ''
    while True:
        sym = port.read(1)
        if sym == b'\r':
            try:
                print(data)
                a = [i for i in data.split()]
                return data + ' {} {} {} {} {} {} {}'.format(a[-3], a[-2], a[-1], *[random.randint(1, 100) for _ in range(4)])
            except:
                pass
        if sym == b'\n':
            data = ''
        else:
            data += str(sym)[2:3]
    data = port.readline()
    return data


def dataOrganize(input_data):
    data = [int(i) for i in input_data.split()]
    n = data[0]
    data = data[1:]
    output_data = [[] for _ in range(n)]
    indexes = []
    for count, index in zip(data[:n], range(n)):
        for _ in range(count):
            indexes.append(index)
    for dat, index in zip(data[n:], indexes):
        output_data[index].append(dat)
    return output_data


def textOutput(labels, data):
    for label, text in zip(labels, data):
        if len(text) > 1:
            label.setText("X:{0}\nY:{1}\nZ:{2}".format(str(text[0]), str(text[1]), str(text[2])))
        else:
            label.setText(str(text[0]))


def widgetOutput(widgets, data):
    for widget, value in zip(widgets, data):
        if type(widget) == list:
            for plot, graph_value in zip(widget, value):
                plot_data = plot.getData()[1]
                plot_data[:-1] = plot_data[1:]
                plot_data[-1] = graph_value
                print(graph_value)
                plot.setData(plot_data)
        else:
            widget.setValue(value[0])


def logsOutput(names, data, log, file, time):
    file.write(str(time)+"s\n")
    log.append(str(time)+"s")
    for name, dat in zip(names, data):
        file.write(f"{name} : {dat}\n")
        log.append(f"{name} : {dat}")
    file.write("----------------\n")
    log.append("----------------")
    
    
def mainLoop():
    #radio_port = serial.Serial("COM5", 115200)
    radio_port = open('file', 'r')
    #file = open('file', 'r')
    log_file = open('logs.txt', 'w')
    time_start = time.time()
    while True:
        try:
            radio_data = radioInput(radio_port)
            #radio_data = radioInput(file)
            data = dataOrganize(radio_data)
            widgets = [[plot1_x, plot1_y, plot1_z], [plot2_x, plot2_y, plot2_z],
                       main.temp1, main.temp2, main.press, main.height]
            text_labels = [main.plot1_text, main.plot2_text, main.temp1_lbl_b,
                           main.temp2_lbl_b, main.press_lbl_b, main.press_lbl_b]
            log_names = ['accel1', 'accel2', 'temp1', 'temp2', 'press', 'height']
            textOutput(text_labels, data)
            widgetOutput(widgets, data)
            logsOutput(log_names, data, main.logs, log_file, time.time()-time_start)
            QtWidgets.QApplication.processEvents()
        except:
            pass"""


class WidgetInfo:
    def __init__(self, widget, text, name, proportion, datatype, type, value_range=[0, 100]):
        self.widget = widget
        self.text = text
        self.name = name
        self.proportion = proportion
        self.datatype = datatype
        self.type = type
        self.value_range = value_range


def radioInput(port):
    """data = []
    while True:
        sym = port.read(1)
        if sym == b'\r':
                print(data)
                return data
        if sym == b'\n':
            data = ''
        else:
            data.append(int(str(sym)[2:3]))"""
    # data = port.readline()
    # return [int(i) for i in data.split()]
    data = [6, 3, 3, 1, 1, 1, 1]
    data += [random.randint(-5, 40) for _ in range(10)]
    return data


def dataOrganize(input_data):
    n = input_data[0]
    data = input_data[1:]
    output_data = [[] for _ in range(n)]
    indexes = []
    for count, index in zip(data[:n], range(n)):
        for _ in range(count):
            indexes.append(index)
    for dat, index in zip(data[n:], indexes):
        output_data[index].append(dat)
    return output_data


def widgetOutput(widget, data):
    if widget.type == 'graph':
        for plot, graph_value in zip(widget.widget, data):
            plot_data = plot.getData()[1]
            plot_data[:-1] = plot_data[1:]
            plot_data[-1] = graph_value * widget.proportion
            plot.setData(plot_data)
    if widget.type == 'bar':
        percent = (data[0] - widget.value_range[0]) * 100 // (widget.value_range[1] - widget.value_range[0])
        widget.widget.setValue(int(percent))


def textOutput(widget, data, file):
    output = [dat * widget.proportion for dat in data]
    if widget.type == 'graph':
        widget.text.setText("X:{0}\nY:{1}\nZ:{2}".format(*[str(i) + widget.datatype for i in output]))
    if widget.type == 'bar':
        widget.text.setText(str(*output) + ' ' + widget.datatype)
    logsWrite(widget.name, data, output, main.logs, file)


def logsWrite(name, input_data, output_data, log, file):
    log.append(f'{name}: {input_data} ---> {output_data}')
    file.write(f'{name}: {input_data} ---> {output_data}\n')


def mainLoop():
    #radio_port = serial.Serial("COM5", 115200)
    radio_port = open('file', 'r')
    log_file = open('logs.txt', 'w')
    time_start = time.time()
    widgets = [WidgetInfo([plot1_x, plot1_y, plot1_z], main.plot1_text, 'accel1', 0.390625, 'м/с', 'graph'),
               WidgetInfo([plot2_x, plot2_y, plot2_z], main.plot2_text, 'accel2', 0.390625, 'м/с', 'graph'),
               WidgetInfo(main.temp1, main.temp1_lbl_b, 'temp1', 1, '°C', 'bar', [-5, 40]),
               WidgetInfo(main.temp2, main.temp2_lbl_b, 'temp2', 1, '°C', 'bar', [-5, 40]),
               WidgetInfo(main.press, main.press_lbl_b, 'press', 101325, 'Па', 'bar', [0.8, 1.2]),
               WidgetInfo(main.height, main.height_lbl_b, 'temp1', 1, 'м', 'bar', [0, 1500])]
    iter = 1
    for i in range(10000):
        radio_data = radioInput(radio_port)
        print(radio_data)
        data = dataOrganize(radio_data)
        input_time = time.time()-time_start
        main.logs.append(f'iter: {iter}')
        main.logs.append(f'input_time: {input_time}')
        log_file.write(f'iter: {iter}\n')
        log_file.write(f'input_time: {input_time}\n')
        for widget, dat in zip(widgets, data):
            widgetOutput(widget, dat)
            textOutput(widget, dat, log_file)
        main.logs.append('-------------------')
        log_file.write('-------------------\n')
        iter += 1
        QtWidgets.QApplication.processEvents()
        time.sleep(0.1)


# pg.setConfigOption('background', 'w')
# pg.setConfigOption('foreground', 'k')
app = QtWidgets.QApplication(sys.argv)
main = MainWindow()
plot1_x = main.plot1.plot(pen='r')
plot1_y = main.plot1.plot(pen='g')
plot1_z = main.plot1.plot(pen='b')
plot2_x = main.plot2.plot(pen='r')
plot2_y = main.plot2.plot(pen='g')
plot2_z = main.plot2.plot(pen='b')
plot1_x.setData([0 for _ in range(25)])
plot1_y.setData([0 for _ in range(25)])
plot1_z.setData([0 for _ in range(25)])
plot2_x.setData([0 for _ in range(25)])
plot2_y.setData([0 for _ in range(25)])
plot2_z.setData([0 for _ in range(25)])
main.LargeButton.clicked.connect(mainLoop)
main.show()
sys.exit(app.exec_())
