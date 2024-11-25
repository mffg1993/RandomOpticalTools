# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 15:46:30 2024

@author: mffg1993
"""

import telegram
from telegram import Bot
import asyncio
import datetime
import time
import numpy as np
import csv
from pylablib.devices import uc480
from pylablib.devices import Thorlabs

# Telegram bot notifier class
class TelegramBotNotifier:
    def __init__(self, bot_token, chat_id):
        """
        Initializes the Telegram bot notifier with the bot token and chat ID.
        
        Parameters:
        bot_token (str): The token of your Telegram bot.
        chat_id (str): Your Telegram chat ID to send messages to.
        """
        self.bot = Bot(token=bot_token)
        self.chat_id = chat_id

    async def send_update(self, message):
        """
        Sends a message to the Telegram chat.

        Parameters:
        message (str): The message to send.
        """
        await self.bot.send_message(chat_id=self.chat_id, text=message)

    async def monitor_measurement(self, measurement_func, *args, **kwargs):
        """
        Monitors the measurement process and sends updates for success or error.

        Parameters:
        measurement_func (function): The function that performs the measurement and saves the data.
        args: Positional arguments to pass to the measurement function.
        kwargs: Keyword arguments to pass to the measurement function.
        """
        try:
            # Perform the measurement with provided parameters
            await measurement_func(*args, **kwargs)  # Call the measurement function with parameters
            
            # Send success message
            await self.send_update("Measurement successful! Data has been saved.")
        
        except Exception as e:
            # Send error message in case of an exception
            await self.send_update(f"Error during measurement: {e}")

# Measurement function to integrate with the notifier
async def LongMeasurement(notifier):
    """
    This function simulates the long-running measurement process
    involving both the camera and the powermeter.
    """

    # Camera setup
    CamNum = uc480.get_cameras_number()
    if CamNum > 0:
        CameraList = uc480.list_cameras()
    else:
        print("There is no camera here!")
        return
    
    for nn in range(CamNum):
        if CameraList[nn].serial_number == 'SERIAL_NUMBER':
            try:
                EOcam = uc480.UC480Camera(CameraList[nn].dev_id)
                break
            except:
                EOcam.close()
                EOcam = uc480.UC480Camera(CameraList[nn].dev_id)

    EOcam.set_exposure(0.1)

    # Powermeter setup
    meter = Thorlabs.PM160('VISA_ADDRESS')

    # Measurement loop
    N = 15  # Number of measurements
    T = 6  # Time between measurements (seconds)
    POW = []  # Power measurement storage

    for nn in range(N):
        # Get the current timestamp
        timestamp = datetime.datetime.now()
        print(timestamp)


        # Name the file for saving the image
        timestr = str(timestamp)[:16].replace(" ", "-").replace(":", "")

        # Take a photo and save it
        img = EOcam.snap()
        np.save("photo" + timestr + ".npy", img)
        
        # Send an update to Telegram after each timestamp is printed
        await notifier.send_update(f"Image saved with Timestamp: {timestamp}")

        # Get the power measurement and save it with the timestamp
        POW.append([meter.get_power(), str(timestamp)])

        # Wait for the specified time
        time.sleep(T)

    # Save the power measurements to a CSV file
    with open("PowerMeasurements"+timestr+".csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(POW)
        await notifier.send_update(f"The Power measurments are ready!")
        

    EOcam.close()
    meter.close()

# Example usage with Telegram bot notifier
async def main():
    # Initialize bot with your bot token and chat ID
    bot_token = 'YOUR_BOT_TOKEN'
    chat_id = 'YOUR_CHAT_ID'
    
    notifier = TelegramBotNotifier(bot_token, chat_id)

    # Notify the start of the measurement
    await notifier.send_update("Starting long measurement...")

    # Monitor the measurement process and notify on success or error
    await notifier.monitor_measurement(LongMeasurement, notifier)

# Use this instead of asyncio.run() in environments like Jupyter or when the event loop is already running
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())  # Schedule the main task
