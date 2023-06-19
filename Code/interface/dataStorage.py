import serial
import pandas as pd

ser = serial.Serial('COM3', 115200, timeout=1)

line = ser.read(10)
print(line)

data = []
while True:
    # line = ser.readline().decode().strip()
    line = ser.read(10)
    data.append(line)
    print(data)
    if len(data) >= 100:
        break

df = pd.DataFrame(data, columns=['Data'])
df.to_csv('data.csv', index=False)
