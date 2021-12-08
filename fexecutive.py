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
file =open("/home/pi/lawn_demo/data_log.cvs","a")

i2c = board.I2C()  # uses board.SCL and board.SDA

bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)
tmp117 = adafruit_tmp117.TMP117(i2c)
icm = adafruit_icm20x.ICM20948(i2c)
ina = INA219(i2c)

bme680.sea_level_pressure = 1013.25
temperature_offset = -5

def cpu_temp():
    temp = os.popen("vcgencmd measure_temp").readline()
    temp = temp.replace("'C","")
    temp = temp.replace("\n","")
    return (temp.replace("temp=",""))

if os.stat("/home/pi/lawn_demo/data_log.cvs").st_size == 0:
    file.write("time,to,ti,gas,hum,press,alt,accx,accy,accz,gyrox,gyroy,gyroz,magnx,magny,magnz,vbus,ibus,pbus,tc\n")

# 3. start wifi hot spot and streaming as a separate process
# TODO: Ugh!

# 4. while loop running with 10 seconds delay after last iteration
#        check power levels (voltage and capacity %)
#        if low
#            attempt to send message over iridium
#            if unsuccessful
#                alert to streaming webpage (???)
#            stop all spawned processes
#            shutdown     
#        read all telemetry values and log them
#        every minute (or every 6th iteration) attempt to send them over iridium

for _ in range(10):
    now = datetime.now()  # TODO: hh:mm only
    data_points = [tmp117.temperature, bme680.temperature, bme680.gas, bme680.relative_humidity, bme680.pressure, bme680.altitude, *icm.acceleration, *icm.gyro, *icm.magnetic, ina.bus_voltage, ina.current, ina.power]
    as_string = ','.join([str(round(d, 2)) for d in data_points])
    file.write(str(now) + ',' + as_string + ',' + cpu_temp())
    file.flush()


file.close()


#
# run("shutdown --poweroff now", shell=True)
#