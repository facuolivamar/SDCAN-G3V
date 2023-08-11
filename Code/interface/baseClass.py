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
            
            'LPG': re.compile(r"LPG = (\d\d.\d\d)"),
            'CH4': re.compile(r"CH4 = (\d\d.\d\d)"),
            'O3': re.compile(r"O3 = (\d\.\d\d\d)"),
            'CO': re.compile(r"CO = (\d\d\d)"),
            'CO2': re.compile(r"CO2 = (\d\d\d)"),
            'NH4': re.compile(r"NH4 = (\d\.\d\d\d)"),
            'Toluen': re.compile(r"Toluen = (\d\d.\d\d)"),
            'Particles': re.compile(r"Particles = (\d\d\d\d)"),
            'Latitude': re.compile(r"Latitude = ([\d.-]+)"),
            'Longitude': re.compile(r"Longitude = ([\d.-]+)"),
            'Speed': re.compile(r"Speed = (\d+)"),
        }

        self.Temperature = self.patternsDict['Temperature'].search(data).group(1)
        self.Pressure = self.patternsDict['Pressure'].search(data).group(1)
        self.Altitude = self.patternsDict['Altitude'].search(data).group(1)
        self.RSSI = self.patternsDict['RSSI'].search(data).group(1)

        try:
            self.LPG = self.patternsDict['LPG'].search(data).group(1)
            self.CH4 = self.patternsDict['CH4'].search(data).group(1)
            self.O3 = self.patternsDict['O3'].search(data).group(1)
            self.CO = self.patternsDict['CO'].search(data).group(1)
            self.CO2 = self.patternsDict['CO2'].search(data).group(1)
            self.NH4 = self.patternsDict['NH4'].search(data).group(1) 
            self.Toluen = self.patternsDict['Toluen'].search(data).group(1)
            self.Particles = self.patternsDict['Particles'].search(data).group(1)
            self.Latitude = self.patternsDict['Latitude'].search(data).group(1)
            self.Longitude = self.patternsDict['Longitude'].search(data).group(1)
            self.Speed = self.patternsDict['Speed'].search(data).group(1)
        except Exception as e:
            print(f'something went wrong with MISION SECUNDARIA values: {e}')



mock_data = "Temperature = 25.65, Pressure = 98765, Altitude = 123.45, RSSI -20, LPG = 45.67, CH4 = 12.34, O3 = 0.045, CO = 123, CO2 = 789, NH4 = 0.005, Toluen = 56.78, Particles = 1234, Latitude = 37.7749, Longitude = -122.4194, Speed = 25"

# Create an instance of dataProcessing with mock data
processed_data = dataProcessing(mock_data)

print("Temperature:", processed_data.Temperature)
print("Pressure:", processed_data.Pressure)
print("Altitude:", processed_data.Altitude)
print("RSSI:", processed_data.RSSI)
print("LPG:", processed_data.LPG)
print("CH4:", processed_data.CH4)
print("O3:", processed_data.O3)
print("CO:", processed_data.CO)
print("CO2:", processed_data.CO2)
print("NH4:", processed_data.NH4)
print("Toluen:", processed_data.Toluen)
print("Particles:", processed_data.Particles)
print("Latitude:", processed_data.Latitude)
print("Longitude:", processed_data.Longitude)
print("Speed:", processed_data.Speed)
