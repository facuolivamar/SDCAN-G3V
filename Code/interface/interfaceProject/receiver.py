import json
import asyncio
import serial
import pandas as pd
import re
import time
import datetime
import os

csv_filename = 'data-receiver-150ms.csv'
csv_directory = 'C:/Users/facun/OneDrive/Documentos/Extra Projects/SDCAN-G3V/Code/interface/interfaceProject'
csv_path = os.path.join(csv_directory, csv_filename)

xlsx_filename = 'data-receiver-150ms.xlsx'
xlsx_directory = 'C:/Users/facun/OneDrive/Documentos/Extra Projects/SDCAN-G3V/Code/interface/interfaceProject'
xlsx_path = os.path.join(xlsx_directory, xlsx_filename)

async def read_serial_data():
    ser = serial.Serial('COM3', 115200, timeout=1)
    
    while True:
        if not ser.isOpen():
            ser.open()

        try:
            data = ser.read(1000).decode('utf-8')
            
            # Define a regular expression pattern to capture the values
            pattern = re.compile(r"Received packet.*?(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+\.\d+)\s+(\d+)\s+(\d+\.\d+)", re.DOTALL)
            # pattern = re.compile(r" *?(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+\.\d+)\s+(\d+)\s+(\d+\.\d+)", re.DOTALL)

            # print(data)
            # Find all matches in the text
            matches = pattern.findall(data)

            # Create a list of dictionaries to hold the data
            data_list = []

            # Process the matches and append them to the list
            for match in matches:
                current_datetime = time.ctime(time.time())
                data_dict = {
                    "datetime": current_datetime,
                    "dust": int(match[0]),
                    "mq135": int(match[1]),
                    "mq131": int(match[2]),
                    "mq4": int(match[3]),
                    "temperature": float(match[4]),
                    "pressure": int(match[5]),
                    "altitude": float(match[6])
                }
                data_list.append(data_dict)

            # Create a DataFrame from the list of dictionaries
            df = pd.DataFrame(data_list)
            
            print(matches)

            # Append the DataFrame to an existing CSV file or create a new one
            if os.path.exists(csv_path):
                df.to_csv(csv_path, mode='a', header=False, index=False)
                print(df)
            else:
                df.to_csv(csv_path, index=False)


        except UnicodeDecodeError as e:
            print(f'UnicodeDecodeError: {e}')

        ser.close()

# Create an asyncio event loop
loop = asyncio.get_event_loop()

# Schedule the serial data reading coroutine to run indefinitely
try:
    loop.run_until_complete(asyncio.gather(
        read_serial_data(),
    ))
except KeyboardInterrupt:
    pass

# Close the event loop
loop.close()
