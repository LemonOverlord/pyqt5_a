import serial


def dw2float(dw_array):
    assert (len(dw_array) == 4)
    dw = int.from_bytes(dw_array, byteorder='little',signed=False)
    s = -1 if (dw >> 31) == 1 \
        else 1                                    # Знак
    e = ( dw >> 23 ) & 0xFF;                      # Порядок
    m = ((dw & 0x7FFFFF ) | 0x800000) if e != 0 \
        else ((dw & 0x7FFFFF ) << 1)              # Мантисса
    m1 = m*(2**(-23))                             # Мантисса в float
    return s*m1*(2**(e-127))


port = serial.Serial("COM5", 112500)
while True:
    # print(dw2float([int(port.read(1)), int(port.read(1)), int(port.read(1)), int(port.read(1))]))
    # print(int.from_bytes(port.read(4), "little"))
    print(port.read(1))


# def dw2float(dw_array):
#     assert (len(dw_array) == 4)
#     dw = int.from_bytes(dw_array, byteorder='little',signed=False)
#     s = -1 if (dw >> 31) == 1 \
#         else 1                                    # Знак
#     e = ( dw >> 23 ) & 0xFF;                      # Порядок
#     m = ((dw & 0x7FFFFF ) | 0x800000) if e != 0 \
#         else ((dw & 0x7FFFFF ) << 1)              # Мантисса
#     m1 = m*(2**(-23))                             # Мантисса в float
#     return s*m1*(2**(e-127))
#
# print(dw2float([0x3e,0x99,0x99,0x9a][::-1]))