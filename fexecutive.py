from subprocess import run

# 1. all necessary imports
import time
import os
import board
import adafruit_bme680
import adafruit_tmp117
import adafruit_icm20x
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219
import psutil
import busio
from time import sleep
from picamera import PiCamera
from datetime import datetime

# TODO: GPS, RockBLOCK, Quadcam array


# 2. setup all components
file =open("/home/pi/EOSS-317/data_log.cvs","a")

i2c = board.I2C()  # uses board.SCL and board.SDA

bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)
tmp117 = adafruit_tmp117.TMP117(i2c)
icm = adafruit_icm20x.ICM20948(i2c)

# i2c = busio.I2C(board.SCL, board.SDA)
i2c_bus = board.I2C()
ina = INA219(i2c_bus)

bme680.sea_level_pressure = 1013.25
temperature_offset = -5

def cpu_temp():
    temp = os.popen("vcgencmd measure_temp").readline()
    temp = temp.replace("'C","")
    temp = temp.replace("\n","")
    return (temp.replace("temp=",""))


# 3. start wifi hot spot and streaming as a separate process
# 4. while loop running with 10 seconds delay after last iteration
#        check power levels (voltage and capacity %)
#        if low
#            attempt to send message over iridium
#            if unsuccessful
#                alert to streaming webpage (???)
#            stop all spawned processes
#            shutdown     
#        read all telemetry values and log them
# if os.stat("/home/pi/EOSS-317/data_log.cvs").st_size == 0:
#      file.write("Time,TMP,Env_temp,gas,humidity,pressure,altitude,acceleration_x,acceleration_y,acceleration_z,gyro_x,gyro_y,gyro_z,magnitometer_x,magnitometer_y,magnitometer_z,CPU_temp,bus_voltage,current,power\n")
#        every minute (or every 6th iteration) attempt to send them over iridium







#
# run("shutdown --poweroff now", shell=True)
#