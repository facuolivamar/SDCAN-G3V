# consumers.py
import json
import asyncio
import serial
import pandas as pd
import re
import time
from .baseClass import dataProcessing
from .models import input

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

import pandas as pd

@database_sync_to_async
def get_db_object():
    return input.objects.get(id = 1)
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

        db_object = await get_db_object()
        # ser = serial.Serial(db_object.serial_port, db_object.baud_rate, timeout=db_object.timeout)

        import sys
        sys.path.insert(0, '../Code/interface/interfaceProject')
        
        csvFile = 'data-receiver.csv'

        while True:
            try:
                # Read data from the serial port
                # if not ser.isOpen():
                    # ser.open()

                # data = ser.read(1000).decode('utf-8')
                data = "Temperature = 25.65, Pressure = 98765, Altitude = 123.45, RSSI -20, LPG = 45.67, CH4 = 12.34, O3 = 0.045, CO = 123, CO2 = 789, NH4 = 0.005, Toluen = 56.78, Particles = 1234, Latitude = 37.7749, Longitude = -122.4194, Speed = 25"

                processed_data = dataProcessing(data)
                
                # Close the serial port connection
                # ser.close()

                df = pd.read_csv(csvFile)
                df.loc[len(df)] = [processed_data.__dict__[key] for key in processed_data.__dict__]
                df.to_csv('data-receiver.csv', index=False)
                
                text_data = processed_data.__dict__
                text_data['altura'] = str(processed_data.calcAltura(db_object.estacion_terrena_altitude)) 
                text_data['estacion_terrena_latitude'] = str(db_object.estacion_terrena_latitude ) 
                text_data['estacion_terrena_longitude'] = str(db_object.estacion_terrena_longitude ) 
                print(text_data)

                await self.send(text_data=json.dumps(text_data))

                await asyncio.sleep(3)

            except Exception as e:
                print(f'Error occurred: {e}')

                await asyncio.sleep(3)
