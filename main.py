import atexit
import serial


def on_exit():
    port.close()


atexit.register(on_exit)

port = serial.Serial("COM5", 115200)
data = ''
while True:
    sym = port.read()
    if sym == b'\r':
        print(data)
    elif sym == b'\n':
        data = ''
    else:
        data += str(ord(str(sym)[2:3]))

dataLength = 2
status = 0

indications = [[] for _ in range(dataLength)]
values = []
file = open("datatxt.txt", "r")
for i in range(dataLength):
    values.append(ord(file.read(1)))
for i in range(len(values)):
    for _ in range(values[i]):
        indications[i].append(ord(file.read(1)))
print(values)
print(indications)
