import serial
import random
from datetime import datetime
import time

# Set baud rate to match the Arduino sketch
baud_rate = 9600

# Set the serial port according to your operating system (adjust as needed)
s = serial.Serial('/dev/cu.usbmodem1101', baud_rate, timeout=20)

while True:  # Infinite loop to keep running continuously
    # Generate a random number between 1 and 5
    number = random.randint(1, 5)
    
    # Send the number to the Arduino, indicating how many times to blink the LED
    time_data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{time_data} Send >>> {number}")
    s.write(bytes(str(number), 'utf-8'))
    time.sleep(number)

    # Update the current time 
    time_data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    num = s.readline().decode('utf-8').strip()

    # Print the current time and the sleep time received from the Arduino
    print(f"{time_data} Arduino sleeps for {num} seconds")
    # Convert the received string to an integer representing the sleep time for the Arduino
    sleepTime = int(num)
    time.sleep(sleepTime)
    
    # Update and print the current time after waking up from the sleep
    time_data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{time_data}: Logs in")
    
    # Print a separator line for clarity
    print("--------------------------------------------")
