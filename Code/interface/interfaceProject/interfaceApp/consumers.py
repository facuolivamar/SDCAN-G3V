# consumers.py
import json
import asyncio
import serial
import pandas as pd
import re
import time


from channels.generic.websocket import AsyncWebsocketConsumer

import pandas as pd

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        # # Send initial data once the connection is established
        # await self.send_initial_data()

        # Start the periodic task to send updates
        asyncio.create_task(self.csv_data_storage())

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # async def send_initial_data(self):
    #     try:
    #         # Generate some data or retrieve it from a source
    #         import sys
    #         sys.path.insert(0, '../Code/interface/interfaceProject')

    #         csvFile = 'data-receiver.csv'
    #         data = pd.read_csv(csvFile)
            
    #         for index in data["datetime"].index:
    #             await self.send(text_data=json.dumps({
    #                 "datetime": str(data["datetime"][index]),
    #                 "temperature": str(data["temperature"][index]),
    #                 "pressure": str(data["pressure"][index]),
    #                 "altitude": str(data["altitude"][index]),
    #                 "rssi": str(data["rssi"][index]),
    #                 }))

    #             await asyncio.sleep(1)
    #     except Exception as e:
    #         print(f"error: {e}")

    async def csv_data_storage(self):
        # Open a connection to the serial port 
               
        ser = serial.Serial('COM3', 115200, timeout=1)

        import sys
        sys.path.insert(0, '../Code/interface/interfaceProject')
        
        csvFile = 'data-receiver.csv'

        while True:
            try:
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

                df = pd.read_csv(csvFile)

                df.loc[len(df)] = [time.ctime(time.time()),temperature, pressure, altitude, rssi]

                # print(df)

                df.to_csv('data-receiver.csv', index=False)

                await self.send(text_data=json.dumps({
                    "datetime": str(time.ctime(time.time())),
                    "temperature": str(temperature),
                    "pressure": str(pressure),
                    "altitude": str(altitude),
                    "rssi": str(rssi),
                    }))

                await asyncio.sleep(3)

            except Exception as e:
                print(f'Error occurred: {e}')

                await asyncio.sleep(3)
