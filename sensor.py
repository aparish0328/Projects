### AIDAN PARISH, APARISH2@CNM.EDU, CREATED FOR INTERNET OF THINGS 101 ###
### This program was created to send sensor data from a dht11 sensor to an online Adafruit.IO dashboard. ###
### It is intended to be used on a Raspberry Pi, and as such, some of the modules used are specific to Raspberry Pi OS and the ARM architecture. ###
### The website/tutorial was referenced during the creation of this code: https://www.jeremymorgan.com/tutorials/raspberry-pi/how-to-iot-adafruit-raspberrypi/ ### 


### MODULES ###
import time
import adafruit_dht
import board
from Adafruit_IO import Client
from subprocess import check_output
from re import findall


### VARIABLES ###
dht = adafruit_dht.DHT11(board.D4)
aio = Client('[your_username_here]','[your_key_here]')    # CHANGE THESE VALUES


### FUNCTIONS ###
def get_temp():
    temp = check_output(["vcgencmd","measure_temp"]).decode("UTF-8")
    return(findall("\d+\.\d+",temp)[0])


### MAIN LOOP ###
while True:
    try:
        ambTemp = (dht.temperature * 9/5) + 32
        smallTemp = round(ambTemp, 2)
        humidity = dht.humidity

        humfeed = aio.feeds('roomhumidity')
        aio.send_data(humfeed.key, humidity)

        tempfeed = aio.feeds('roomtemp')
        aio.send_data(tempfeed.key, smallTemp)

        cpu_temp = get_temp()
        cpufeed = aio.feeds('cputemp')
        aio.send_data(cpufeed.key, cpu_temp)
        
        RAM = check_output(["free"]).decode("UTF-8")
        ramfeed = aio.feeds('ram')
        aio.send_data(ramfeed.key, RAM)

    except RuntimeError as e:
        print("Reading failure: ", e.args)
    time.sleep(30)

### END ###