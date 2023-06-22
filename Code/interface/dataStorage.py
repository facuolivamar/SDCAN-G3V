import serial
import pandas as pd
import re

try:
    # Open a connection to the serial port
    ser = serial.Serial('COM11', 115200, timeout=1)

    # Read data from the serial port
    if not ser.isOpen():
        ser.open()

    data = ser.read(1000).decode('utf-8')

    # print(f"Received data: {data}")

    temperaturePattern = re.compile(r"Temperature = (\d\d.\d\d)")
    temperature = temperaturePattern.search(data).group(1)

    pressurePattern = re.compile(r"Pressure = (\d\d\d\d\d)")
    pressure = pressurePattern.search(data).group(1)

    altitudePattern = re.compile(r"Altitude = (\d\d\d.\d\d)")
    altitude = altitudePattern.search(data).group(1)

    rssiPattern = re.compile(r"RSSI (-\d\d)")
    rssi = rssiPattern.search(data).group(1)

    # print(f"Packet: {packet}")
    print(f"Temperature: {temperature}")
    print(f"Pressure: {pressure}")
    print(f"Altitude: {altitude}")
    print(f"RSSI: {rssi}")
    
    # Close the serial port connection
    ser.close()

except Exception as e:
    print(f'Error occurred: {e}')
