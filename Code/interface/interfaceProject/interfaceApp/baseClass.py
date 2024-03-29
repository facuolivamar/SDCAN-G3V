import json
import asyncio
import serial
import pandas as pd
import re
import time

# ----------------------------------
# ---------- Received packet  -------
# 2203
# 0
# 0
# 39
# 22.10
# 96663
# 395.23
# ----------------------------------
# ---------- Received packet  -------

class dataProcessing():

    def __init__(self, data) -> None:
        patternsDict = {
            'Temperature' : re.compile(r"Temperature = (\d\d.\d\d)"),
            'Pressure' : re.compile(r"Pressure = (\d\d\d\d\d)"),
            'Altitude' : re.compile(r"Altitude = (\d\d\d.\d\d)"),
            'RSSI' : re.compile(r"RSSI (-\d\d)"),

            'NO2': re.compile(r"LPG = (\d.\d\d\d)"),
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
        
        self.datetime = time.ctime(time.time())

        self.Temperature = patternsDict['Temperature'].search(data).group(1)
        self.Pressure = patternsDict['Pressure'].search(data).group(1)
        self.Altitude = patternsDict['Altitude'].search(data).group(1)
        self.RSSI = patternsDict['RSSI'].search(data).group(1)

        try:
            # self.NO2 = patternsDict['NO2'].search(data).group(1)
            self.LPG = patternsDict['LPG'].search(data).group(1)
            self.CH4 = patternsDict['CH4'].search(data).group(1)
            self.O3 = patternsDict['O3'].search(data).group(1)
            self.CO = patternsDict['CO'].search(data).group(1)
            self.CO2 = patternsDict['CO2'].search(data).group(1)
            self.NH4 = patternsDict['NH4'].search(data).group(1) 
            self.Toluen = patternsDict['Toluen'].search(data).group(1)
            self.Particles = patternsDict['Particles'].search(data).group(1)
            self.Latitude = patternsDict['Latitude'].search(data).group(1)
            self.Longitude = patternsDict['Longitude'].search(data).group(1)
            self.Speed = patternsDict['Speed'].search(data).group(1)
        except Exception as e:
            print(f'something went wrong with MISION SECUNDARIA values: {e}')

    def calcAltura(self, x0):
        '''
        Calcular altura respecto a valor de altitud al momento de despege(y0), y al valor de altitud en el momento actual.
        '''
        altura = float(self.Altitude) - float(x0)

        return altura

    # def calcNOx(self, x):
    #     NOx = x

    #     return NOx

    # def calcCOVs(self, x):
    #     COVs = x

    #     return COVs

    # def calcO3(self, x):
    #     O3 = x

    #     return O3

    # def calcCO2(self, x):
    #     CO2 = x

    #     return CO2
    
    def calcAirQuality(self, x):
        '''
        Calculate air quality based on US EPA criteria
        '''
        calcs_result = float

        air_quality_level = int

        quality_index = {
            '50' : 1,
            '100' : 2,
            '200' : 3,
            '300' : 4,
            '400' : 5,
        }
        
        for key in quality_index:
            if calcs_result < key:
                air_quality_level = quality_index[key]

        return air_quality_level



# mock_data = "Temperature = 25.65, Pressure = 98765, Altitude = 123.45, RSSI -20, LPG = 45.67, CH4 = 12.34, O3 = 0.045, CO = 123, CO2 = 789, NH4 = 0.005, Toluen = 56.78, Particles = 1234, Latitude = 37.7749, Longitude = -122.4194, Speed = 25"

# # Create an instance of dataProcessing with mock data
# processed_data = dataProcessing(mock_data)

# print(processed_data.calcAltura.__doc__)

# print("Temperature:", processed_data.Temperature)
# print("Pressure:", processed_data.Pressure)
# print("Altitude:", processed_data.Altitude)
# print("RSSI:", processed_data.RSSI)
# print("LPG:", processed_data.LPG)
# print("CH4:", processed_data.CH4)
# print("O3:", processed_data.O3)
# print("CO:", processed_data.CO)
# print("CO2:", processed_data.CO2)
# print("NH4:", processed_data.NH4)
# print("Toluen:", processed_data.Toluen)
# print("Particles:", processed_data.Particles)
# print("Latitude:", processed_data.Latitude)
# print("Longitude:", processed_data.Longitude)
# print("Speed:", processed_data.Speed)

# print(processed_data.__dict__)

# text_data = processed_data.__dict__
# x = [key for key in text_data]
# print(x)

# print(text_data)

# import sys
# sys.path.insert(0, '../Code/interface/interfaceProject')
        
# csvFile = 'data-receiver.xlsx'

# import pandas as pd
# df = pd.DataFrame(columns=x)
# new_row = {key: processed_data.__dict__[key] for key in processed_data.__dict__}
# df = df._append(new_row, ignore_index=True)
# df.to_excel(csvFile, index=False)
