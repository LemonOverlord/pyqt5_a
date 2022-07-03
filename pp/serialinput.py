
# import serial
# ser=serial.Serial('/dev/ttyACM0',115200)
# while True:
#     value = float(ser.readline().strip())
#     print('{0:0.2f}'.format(value))

# import struct
#
# print(*struct.unpack("f", 0x3f800000.to_bytes(4, "little")))
import struct
import serial

print((1).to_bytes(1, "little"))
print((11).to_bytes(1, "little"))
print((16).to_bytes(1, "little"))
print((1000).to_bytes(2, "little"))
print((33).to_bytes(1, "little"))
print((100).to_bytes(1, "little"))

print(bin(100))
print(0x3f800000.to_bytes(4, "little"))

print(struct.unpack("b", b'\x79'))
# 3f 00111111 80 1000000 00 00000000 00 00000000
#

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