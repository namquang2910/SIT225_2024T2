import csv
import serial
import random
from datetime import datetime
import time

# Set the serial port according to your operating system (adjust as needed)
s = serial.Serial('/dev/cu.usbmodem1101', 9600, timeout=20)

#Name the file
filename = 'test.csv'

# Create a CSV file and write the header
#with open(filename, 'w', newline='') as file:
 #   writer = csv.writer(file)
    # Write the header
  #  writer.writerow(["Timestamp", "Temperature", "Humidity"])

while True:  
    # Get the current time and read the data from the Arduino
    time_current = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = s.readline().decode('utf-8').strip()
    tempHum = line.split(",")

    #Create a list of data to write to the CSV file
    data = [time_current, tempHum[1], tempHum[0]]

    # Write data to the CSV file
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        # Write the data rows
        writer.writerow(data)
