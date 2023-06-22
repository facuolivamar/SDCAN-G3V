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

        # Send initial data once the connection is established
        await self.send_initial_data()

        # Start the periodic task to send updates
        asyncio.create_task(self.send_updates())

        asyncio.create_task(self.csv_data_storage())

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def send_initial_data(self):
        # Generate some data or retrieve it from a source
        import sys
        sys.path.insert(0, '../Code/interface/interfaceProject')

        dataFile = "machine-readable-business-employment-data-mar-2023-quarter.csv"
        data = pd.read_csv(dataFile)

        cont = 0
        while cont < 10:
            value = float(data["Data_value"][cont])

            # Send the data to the WebSocket
            await self.send(text_data=json.dumps({"value": value, "index": cont}))

            cont += 1

            # Wait for a few seconds before sending the next update
            await asyncio.sleep(1)

    async def send_updates(self):
        cont = 10
        while True:
            # Generate some data or retrieve it from a source
            import sys
            sys.path.insert(0, '../Code/interface/interfaceProject')


            dataFile = "machine-readable-business-employment-data-mar-2023-quarter.csv"
            data = pd.read_csv(dataFile)
            
            value = float(data["Data_value"][cont])

            # Send the data to the WebSocket
            await self.send(text_data=json.dumps({"value": value, "index":cont}))
            
            cont += 1

            # Wait for a few seconds before sending the next update
            await asyncio.sleep(5)

    async def csv_data_storage(self):
        # Open a connection to the serial port
        ser = serial.Serial('COM11', 115200, timeout=1)

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

                print(df)

                df.to_csv('Code/interface/interfaceProject/data-receiver.csv', index=False)
                
                await asyncio.sleep(0.5)

            except Exception as e:
                print(f'Error occurred: {e}')

