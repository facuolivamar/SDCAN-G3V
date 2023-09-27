import json
import asyncio
import serial
import pandas as pd
import re
import time
import datetime

async def read_serial_data():
    ser = serial.Serial('COM3', 115200, timeout=1)
    count = 0
    dataDict = {}
    
    while True:
        if not ser.isOpen():
            ser.open()

        try:
            data = ser.read(1000).decode('utf-8')
            dataDict[time.ctime(time.time()) ] = data
            
            # Define a regular expression pattern to capture the values
            pattern = re.compile(r"Received packet.*?(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+\.\d+)\s+(\d+)\s+(\d+\.\d+)", re.DOTALL)

            # Find all matches in the text
            matches = pattern.findall(data )

            # Define the column names
            columns = ["dust", "mq135", "mq131", "mq4", "temperature", "pressure", "altitude"]

            # Print the header
            print(", ".join(columns))

            print(matches)
            # Print the captured values
            for match in matches:
                # Convert the values to strings and join them with commas
                row = ", ".join(map(str, match))
                print(row)
                
            


            count += 1
            if count >= 10:
                print(f'count: {count}')
                print(time.time() - varTime)
                break
        except UnicodeDecodeError as e:
            print(f'UnicodeDecodeError: {e}')

        ser.close()

# Store the start time
varTime = time.time()

# Create an asyncio event loop
loop = asyncio.get_event_loop()

# Schedule the serial data reading coroutine to run every 150 milliseconds
try:
    loop.run_until_complete(asyncio.gather(
        read_serial_data(),
        asyncio.sleep(0.15),  # Sleep for 150 milliseconds
    ))
except KeyboardInterrupt:
    pass

# Close the event loop
loop.close()

exit()