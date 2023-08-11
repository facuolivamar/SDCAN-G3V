import json
import asyncio
import serial
import pandas as pd
import re
import time


class dataProcessing():

    def __init__(self, data) -> None:
        self.patternsDict = {
            'Temperature' : re.compile(r"Temperature = (\d\d.\d\d)"),
            'Pressure' : re.compile(r"Pressure = (\d\d\d\d\d)"),
            'Altitude' : re.compile(r"Altitude = (\d\d\d.\d\d)"),
            'RSSI' : re.compile(r"RSSI (-\d\d)"),
        }

        self.Temperature = self.patternsDict['Temperature'].search(data).group(1)
        self.Pressure = self.patternsDict['Pressure'].search(data).group(1)
        self.Altitude = self.patternsDict['Altitude'].search(data).group(1)


        self.RSSI = self.patternsDict['RSSI'].search(data).group(1)


mock_data = "Temperature = 25.65, Pressure = 98765, Altitude = 123.45, RSSI -20"

# Create an instance of dataProcessing with mock data
processed_data = dataProcessing(mock_data)

# Print the extracted values
print("Temperature:", processed_data.Temperature)
print("Pressure:", processed_data.Pressure)
print("Altitude:", processed_data.Altitude)
print("RSSI:", processed_data.RSSI)
