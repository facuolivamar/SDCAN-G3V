# consumers.py
import json
import asyncio
import serial
import pandas as pd
import re
import time
from .baseClass import dataProcessing
from .models import input

import os

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

import pandas as pd

from .processing import processingClass

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

    async def csv_data_storage(self):
        # Open a connection to the serial port 

        # import sys
        # sys.path.insert(0, '../Code/interface/interfaceProject')
        
        # csvFile = 'data-receiver.csv'
        # xlsxFile = 'data-receiver.xlsx'
        
        
        csv_filename = 'data-receiver-150ms.csv'
        csv_directory = 'C:/Users/facun/OneDrive/Documentos/Extra Projects/SDCAN-G3V/Code/interface/interfaceProject'
        csv_path = os.path.join(csv_directory, csv_filename)


        while True:
            try:

                
                df = pd.read_csv(csv_path, on_bad_lines='skip')
                last_row = df.iloc[len(df)-1].to_dict()

                obj = processingClass(dict(last_row))
                
                text_data = obj.__dict__
                text_data['datetime'] = last_row['datetime']
                # text_data['altura'] = str(processed_data.calcAltura(db_object.estacion_terrena_altitude)) 
                # text_data['estacion_terrena_latitude'] = str(db_object.estacion_terrena_latitude ) 
                # text_data['estacion_terrena_longitude'] = str(db_object.estacion_terrena_longitude ) 
                
                # print(text_data + last_row)
                
                for key, value in last_row.items():
                    # if key in text_data:
                    #     text_data[key] += value
                    # else:
                    text_data[key] = value

                print(text_data)
                await self.send(text_data=json.dumps(text_data))

                await asyncio.sleep(1)

            except Exception as e:
                print(f'Error occurred: {e}')

                await asyncio.sleep(3)
