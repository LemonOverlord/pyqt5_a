import serial


port = serial.Serial('COM6', 115200)
word = ''
while True:
    sym = port.read()
    if sym == b'\r':
        pass
    if sym == b'\n':
        word = ''
    else:
        word += str(sym)[2:3]