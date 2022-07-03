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
from PyQt5.QtGui import QImage, QPalette, QBrush, QPixmap


class Window(QtWidgets.QMainWindow):
    # t1: Thread
    # t2: Thread
    def __init__(self, ui_name, win_name, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        # Загрузите страницу интерфейса
        uic.loadUi(ui_name, self)
        self.setWindowTitle(win_name)

    # def cameraInit(self):
    #     oImage = QImage("cat3.png")
    #     sImage = oImage.scaled(QSize(300, 200))
    #     palette = QPalette()
    #     palette.setBrush(QPalette.Window, QBrush(sImage))
    #     self.setPalette(palette)


class SensorInfo:
    def __init__(self, plot_place, text_place, plot_lst):
        self.plot_place = plot_place
        self.text_place = text_place
        self.plot_lst = plot_lst


class Plot:
    def __init__(self, plot, data_name, data_type):
        self.plot = plot
        self.data_name = data_name
        self.data_type = data_type


def portReadSensor(port: serial.Serial, data_type : str, data_scale : int, iterations : int):
    result = []
    for _ in range(iterations):
        result.append(*struct.unpack(data_type, port.read(data_scale)))


def portRead(port: serial.Serial):
    sym = port.read(1)
    binar = bin(*struct.unpack("b", sym))
    if str(binar)[2:4] == "00":
        return {"DS18B20": portReadSensor(port, "f", 4, 1)}
    elif str(binar)[2:4] == "01":
        return {"BMP280": portReadSensor(port, "f", 4, 2)}
    elif str(binar)[2:4] == "10":
        return {"ADXL345": portReadSensor(port, "i", 2, 3), "HMC5883MA": portReadSensor(port, "f", 4, 3),
                "L3G4200D": portReadSensor(port, "f", 4, 3)}
    else:
        pass


def fileRead(file):
    data = [int(i) for i in file.readline().split()]
    if data == "":
        return "end"
    if data[0] == 0:
        return {"DS18B20": data[1:]}
    elif data[0] == 1:
        return {"BMP280": data[1:]}
    else:
        return {"ADXL345": data[1:4], "HMC5883MA": data[4:7], "L3G4200D": data[7:]}


def plotOutputPort(data):
    for sensor in data.keys():
        for i in range(len(data[sensor])):
            plot_data = list(sensors[sensor].plot_lst[i].plot.getData()[1])
            plot_data[:-1] = plot_data[1:]
            plot_data[-1] = data[sensor][i]
            sensors[sensor].plot_lst[i].plot.setData(plot_data)


def plotOutputFile(data):
    for sensor in data.keys():
        for i in range(len(data[sensor])):
            plot_data = list(sensors[sensor].plot_lst[i].plot.getData()[1])
            plot_data.append(data[sensor][i])
            sensors[sensor].plot_lst[i].plot.setData(plot_data)


def textOutput(data):
    for sensor in data.keys():
        text = ""
        for i in range(len(data[sensor])):
            text += sensors[sensor].plot_lst[i].data_name + \
                    str(data[sensor][i]) + \
                    sensors[sensor].plot_lst[i].data_type + \
                    "\n"
        sensors[sensor].text_place.setText(text)


def logsOutput(data):
    for sensor in data.keys():
        main.log_frame.append(f"{sensor}: {data[sensor]}")
    main.log_frame.append("-------------------")


def fileWrite(file, data):
    keys = data.keys()
    text = ""
    for sym in data[keys[0]]:
        text += str(sym)
    if keys[0] == "DS18B20":
        file.write(f"0 {text}")
    elif keys[0] == "BMP280":
        file.write(f"1 {text}")
    else:
        file.write(f"2 {text}")


def scenarioPort():
    port = serial.Serial(reg.portName.text(), int(reg.portSpeed.text()))
    file = open("file.txt", "w")

    for sensor in sensors.keys():
        for plot in sensors[sensor].plot_lst:
            plot.plot.setData([0 for _ in range(25)])

    main.show()
    reg.close()

    while True:
        data = portRead(port)
        plotOutputPort(data)
        textOutput(data)
        logsOutput(data)
        fileWrite(file, data)

        QtWidgets.QApplication.processEvents()


def scenarioFile():
    file = open(reg.fileName.text(), "r")

    for sensor in sensors.keys():
        for plot in sensors[sensor].plot_lst:
            plot.plot.setData([0])

    main.show()
    camera.show()
    reg.close()

    while True:
        data = fileRead(file)
        if data == "end":
            break
        plotOutputFile(data)
        textOutput(data)
        logsOutput(data)

        QtWidgets.QApplication.processEvents()

    while True:
        QtWidgets.QApplication.processEvents()


app = QtWidgets.QApplication(sys.argv)
main = Window("dataWindow.ui", "Data")
reg = Window("regWindow.ui", "Input")
camera = Window("cameraWindow.ui", "Camera(Cat)")

# camera.cameraInit()

reg.connectButton.clicked.connect(scenarioPort)
reg.readButton.clicked.connect(scenarioFile)

sensors = {"ADXL345": SensorInfo(main.adxl345_plotplace, main.adxl345_textplace,
                                 [Plot(main.adxl345_plotplace.plot(pen="r"), "X:", "м/с²"),
                                  Plot(main.adxl345_plotplace.plot(pen="g"), "Y:", "м/с²"),
                                  Plot(main.adxl345_plotplace.plot(pen="b"), "Z:", "м/с²")]),
           "DS18B20": SensorInfo(main.ds18b20_plotplace, main.ds18b20_textplace,
                                 [Plot(main.ds18b20_plotplace.plot(pen="w"), "temp:", "°C")]),
           "BMP280": SensorInfo(main.bmp280_plotplace, main.bmp280_textplace,
                                [Plot(main.bmp280_plotplace.plot(pen="m"), "temp:", "°C"),
                                 Plot(main.bmp280_plotplace.plot(pen="y"), "press:", "Па")]),
           "HMC5883MA": SensorInfo(main.hmc5883ma_plotplace, main.hmc5883ma_textplace,
                                   [Plot(main.hmc5883ma_plotplace.plot(pen="r"), "X:", "Попугаев"),
                                    Plot(main.hmc5883ma_plotplace.plot(pen="g"), "Y:", "Попугаев"),
                                    Plot(main.hmc5883ma_plotplace.plot(pen="b"), "Z:", "Попугаев")]),
           "L3G4200D": SensorInfo(main.l3g4200d_plotplace, main.l3g4200d_textplace,
                                  [Plot(main.l3g4200d_plotplace.plot(pen="r"), "X:", "Попугаев"),
                                   Plot(main.l3g4200d_plotplace.plot(pen="g"), "Y:", "Попугаев"),
                                   Plot(main.l3g4200d_plotplace.plot(pen="b"), "Z:", "Попугаев")])}

reg.show()
sys.exit(app.exec_())