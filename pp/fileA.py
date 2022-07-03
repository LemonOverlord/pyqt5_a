import random
import struct
import sys
import threading
import time
import asyncio
import regex
from threading import Thread

import pyqtgraph.PlotData
import serial
from PyQt5 import QtWidgets, uic
from pyqtgraph.Qt import QtGui
import pyqtgraph as pg
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush


class Window(QtWidgets.QMainWindow):
    # t1: Thread
    # t2: Thread
    def __init__(self, ui_name, win_name, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        # Загрузите страницу интерфейса
        uic.loadUi(ui_name, self)
        self.setWindowTitle(win_name)


class GraphInfo:
    def __init__(self, plots_lst, text_place, data_name, k, data_type):
        self.plot_lst = plots_lst
        self.text_place = text_place
        self.data_name = data_name
        self.k = k
        self.data_type = data_type


def portReadDS18B20(port: serial.Serial):
    return [*struct.unpack("f", port.read(4))]

def portReadBMP280(port: serial.Serial):
    return [*struct.unpack("f", port.read(4)), *struct.unpack("f", port.read(4))]

def portReadADXL345(port: serial.Serial):
    return [*struct.unpack("i", port.read(2)), *struct.unpack("i", port.read(2)), *struct.unpack("i", port.read(2))]

def portReadHMC5883MA_L3G4200D(port: serial.Serial):
    return [*struct.unpack("f", port.read(4)), *struct.unpack("f", port.read(4)), *struct.unpack("f", port.read(4))]

def portRead(port: serial.Serial):
    sym = port.read(1)
    binar = bin(*struct.unpack("b", sym))
    if str(binar)[2:4] == "00":
        return {"DS18B20": portReadDS18B20(port)}
    elif str(binar)[2:4] == "01":
        return {"BMP280": portReadBMP280(port)}
    elif str(binar)[2:4] == "10":
        return {"ADXL345": portReadADXL345(port), "HMC5883MA" : portReadHMC5883MA_L3G4200D(port),
                "L3G4200D" : portReadHMC5883MA_L3G4200D(port)}
    else:
        pass



def fileRead(file):
    line = file.readline()
    data = {"adxl": [], "temp": [], "press": [], "magnit": [], "gyro": []}
    for name in names:
        if line == '':
            return "end"
        data[name] = [int(i) for i in line.split()]
        line = file.readline()
    return data


# def fileRead(file):
#     data = {"adxl" : [], "temp" : [], "press" : [], "monsoon" : [], "gyro" : []}
#     line = file.readline()
#     while line != "-------------------":
#


def dataOrganize(data):
    data = {"adxl": data["A"], "temp": [data["W"][1], data["W"][0]], "press": [data["W"][2]], "magnit": data["M"],
            "gyro": data["G"]}
    return 0


# def cookData(raw_data):
#     cooked_data = {"adxl": [], "temp": [], "press": [], "monsoon": [], "gyro": []}
#     for name in names:
#         for value in raw_data[name]:
#             cooked_data[name].append(value * graphs[name].k)
#     return cooked_data


def plotOutputPort(values):
    for name in names:
        for plot, value in zip(graphs[name].plot_lst, values[name]):
            plot_data = plot.getData()[1]
            plot_data[:-1] = plot_data[1:]
            plot_data[-1] = value
            plot.setData(plot_data)


def plotOutputFile(data):
    for name in names:
        for plot, dat in zip(graphs[name].plot_lst, data[name]):
            plot_data = list(plot.getData()[1])
            plot_data.append(dat)
            plot.setData(plot_data)


def textOutput(values):
    for name in names:
        text = ""
        for data_name, value in zip(graphs[name].data_name, values[name]):
            text += data_name + str(value) + graphs[name].data_type + "\n"
        graphs[name].text_place.setText(text)


def logOutput(values_raw, file=None):
    for name in names:
        log_file_text = ""
        main.logs.append(f'{name}: {values_raw[name]}')
        if file is not None:
            for value in values_raw[name]:
                log_file_text += " " + str(value)
            file.write(name + ":" + log_file_text)
    main.logs.append('-------------------')
    if file is not None:
        file.write('-------------------')


def scenarioPort():
    port = serial.Serial(reg.portName.text(), int(reg.portSpeed.text()))
    file = open("file.txt", "w")

    x.setData([0 for _ in range(25)])
    y.setData([0 for _ in range(25)])
    z.setData([0 for _ in range(25)])
    temp1.setData([0 for _ in range(25)])
    temp2.setData([0 for _ in range(25)])
    press_plot.setData([0 for _ in range(25)])
    monsoon_x.setData([0 for _ in range(25)])
    monsoon_y.setData([0 for _ in range(25)])
    monsoon_z.setData([0 for _ in range(25)])
    gyro_x.setData([0 for _ in range(25)])
    gyro_y.setData([0 for _ in range(25)])
    gyro_z.setData([0 for _ in range(25)])

    main.show()
    reg.close()
    while True:
        data_raw = portRead(port)
        dataOrganize(data_raw)
        #data_cooked = cookData(data_raw)
        plotOutputPort(data_raw)
        textOutput(data_raw)
        logOutput(data_raw, file)


def scenarioFile():
    file = open(reg.fileName.text(), "r")
    main.show()
    reg.close()
    while True:
        data_raw = fileRead(file)
        if data_raw == "end":
            break
        #data_cooked = cookData(data_raw)
        plotOutputFile(data_raw)
        textOutput(data_raw)
        logOutput(data_raw)
        QtWidgets.QApplication.processEvents()
    while True:
        QtWidgets.QApplication.processEvents()


app = QtWidgets.QApplication(sys.argv)
main = Window("outputWindow.ui", "Output")
reg = Window("regWindow.ui", "Input")

reg.connectButton.clicked.connect(scenarioPort)
reg.readButton.clicked.connect(scenarioFile)

x = main.adxl.plot(pen="r")
y = main.adxl.plot(pen="g")
z = main.adxl.plot(pen="b")
temp1 = main.temp.plot(pen="m")
temp2 = main.temp.plot(pen="y")
press_plot = main.press.plot(pen="w")
monsoon_x = main.monsoon.plot(pen="r")
monsoon_y = main.monsoon.plot(pen="g")
monsoon_z = main.monsoon.plot(pen="b")
gyro_x = main.gyro.plot(pen="r")
gyro_y = main.gyro.plot(pen="g")
gyro_z = main.gyro.plot(pen="b")

x.setData([0])
y.setData([0])
z.setData([0])
temp1.setData([0])
temp2.setData([0])
press_plot.setData([0])
monsoon_x.setData([0])
monsoon_y.setData([0])
monsoon_z.setData([0])
gyro_x.setData([0])
gyro_y.setData([0])
gyro_z.setData([0])

adxl = GraphInfo([x, y, z], main.adxl_text, ["X:", "Y:", "Z:"], 1, "м/с²")
temp = GraphInfo([temp1, temp2], main.temp_text, ["temp1:", "temp2:"], 1, "°C")
press = GraphInfo([press_plot], main.press_text, ["press:"], 1, "Па")
monsoon = GraphInfo([monsoon_x, monsoon_y, monsoon_z], main.monsoon_text, ["X:", "Y:", "Z:"], 1, "Попугаев")
gyro = GraphInfo([gyro_x, gyro_y, gyro_z], main.gyro_text, ["X:", "Y:", "Z:"], 1, "Попугаев")

names = ["ADXL345", "DS18B20", "BMP280", "HMC5883MA", "L3G4200D"]
graphs = {"ADXL345": adxl, "DS18B20": temp, "BMP280": press, "magnit": monsoon, "gyro": gyro}

reg.show()
sys.exit(app.exec_())
