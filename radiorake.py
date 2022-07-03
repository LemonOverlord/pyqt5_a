import serial
import regex

ser = serial.Serial('COM6', 115200)

result = {
    'A': [0, 0, 0],
    'G': [0, 0, 0],
    'W': [0, 0, 0],
    'M': [0, 0, 0]
}

while True:
    try:
        line = ser.readline()
        if line:
            string = line.decode()
            for letter in regex.findall(r'.:[0-9\s\-\.]{1,}', string):
                result[letter[0]] = list(map(float, letter[2:].split()))
            print(f"Акселерометр ADXL345: \t{result['A']}")
            print(f"Гироскоп L3G4200D:    \t{result['G']}")
            print(f"Магнитометр MMC5883MA:\t{result['M']}")
            print(f"Температура BMP280:   \t{result['W'][1]}")
            print(f"Температура DS18B20:  \t{result['W'][0]}")
            print(f"Давление BMP280:      \t{result['W'][2]}")
    except Exception:
        pass
