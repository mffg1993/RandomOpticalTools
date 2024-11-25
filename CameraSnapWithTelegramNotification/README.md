# Using a Telegram Bot to keep track of multiple measurements

This repository contains a script to control a scientific setup involving an IDS camera  and a Thorlabs power meter (Thorlabs PM160). The script takes periodic measurements, including snapshots and power readings, and saves the data. It also integrates a Telegram bot to send notifications during the measurement process.

## Features
- **Camera Control**: Detects and communicates with the Edmund Optics camera. Snapshots are taken at each measurement cycle and saved as numpy arrays.
- **Power Meter Control**: Reads power data from the Thorlabs PM160 and logs it with timestamps.
- **Periodic Measurements**: Takes multiple measurements with user-defined intervals between each.
- **Telegram Bot Notifications**: Sends updates to a Telegram chat whenever:
  - A new measurement cycle starts.
  - Each timestamp is printed during the loop.
  - The entire measurement process is completed.
  - Any errors occur during the measurement process.

## Requirements

### Python Libraries
The following libraries are required:
- `pylablib`: For controlling the Edmund Optics camera and Thorlabs powermeter.
- `numpy`: For saving images as numpy arrays.
- `csv`: For saving power data in CSV format.
- `datetime`: For timestamp management.
- `time`: For handling delays between measurements.
- `telegram`: For integrating Telegram bot notifications.
- `asyncio`: For asynchronous programming with the Telegram bot.

### Devices
- **Edmund Optics Camera**
- **Thorlabs PM160 Power Meter**

## Installation

1. **Install Dependencies**:
   Use `pip` to install the required Python libraries:
   ```bash
   pip install numpy pylablib python-telegram-bot
   ```

2. **Configure the Telegram Bot**:
   - Create a Telegram bot using [BotFather](https://core.telegram.org/bots#botfather) and obtain your bot token.
   - Send a message to your bot to initiate a conversation.
   - Use the script to obtain your chat ID (details below).

## Usage

1. **Configure Device Settings**:
   - Ensure the Edmund Optics camera and Thorlabs power meter are connected.
   - Modify the camera serial number (`'Serial_Number'`) and the VISA address for the power meter (`'VISA_ADDRESS'`) as needed.

2. **Update the Telegram Bot Credentials**:
   - Replace `'YOUR_BOT_TOKEN'` and `'YOUR_CHAT_ID'` in the script with your actual bot token and chat ID.

3. **Telegram Notifications**:
   You will receive messages on Telegram for the following:
   - When the measurement starts.
   - After each timestamp is printed during the measurement process.
   - When the measurement is completed.
   - If any error occurs during the process.

## Example

An example of what a Telegram update might look like:

- **Start Message**:  
  _Starting long measurement..._

- **Measurement Cycle Updates**:  
  _Timestamp: 2024-10-03 12:34:56.789123_

- **Completion Message**:  
  _Measurement successful! Data has been saved._

- **Error Handling**:  
  If any errors occur during the measurement process, a detailed message will be sent with the exception information.

## Contributing
