# consumers.py
import json
import asyncio

from channels.generic.websocket import AsyncWebsocketConsumer

import pandas as pd

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        # Start the periodic task to send updates
        asyncio.create_task(self.send_updates())

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

    async def send_updates(self):
        cont = 0
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
