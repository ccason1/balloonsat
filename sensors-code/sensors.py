
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

file =open("/home/pi/EOSS-317/data_log.cvs","a")

i2c = board.I2C()  # uses board.SCL and board.SDA
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)
tmp117 = adafruit_tmp117.TMP117(i2c)
icm = adafruit_icm20x.ICM20948(i2c)

# TODO: ???
#i2c = busio.I2C(board.SCL, board.SDA)

# TODO: ???
# i2c_bus = board.I2C()
# ina = INA219(i2c_bus)

ina = INA219(i2c)

camera = PiCamera()
#loop_counter = 1
bme680.sea_level_pressure = 1013.25
i = 0
video_count = 0
temperature_offset = -5
def cpu_temp():
    temp = os.popen("vcgencmd measure_temp").readline()
    temp = temp.replace("'C","")
    temp = temp.replace("\n","")
    return (temp.replace("temp=",""))

if os.stat("/home/pi/EOSS-317/data_log.cvs").st_size == 0:
     file.write("Time,TMP,Env_temp,gas,humidity,pressure,altitude,acceleration_x,acceleration_y,acceleration_z,gyro_x,gyro_y,gyro_z,magnitometer_x,magnitometer_y,magnitometer_z,CPU_temp,bus_voltage,current,power\n")

camera.start_recording('/home/pi/EOSS-317/testvideo%s.h264' % video_count)

while True:
#     print("Temperature: %.2f degrees C" % tmp117.temperature)
#     print("Environmental Temperature : %.2f degrees C" % bme680.temperature)
#     print("Gas: %d ohm" % bme680.gas)
#     print("Humidity: %0.1f %%" % bme680.relative_humidity)
#     print("Pressure: %0.3f hPa" % bme680.pressure)
#     print("Altitude = %0.2f meters" % bme680.altitude)
#     print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (icm.acceleration))
#     print("Gyro X:%.2f, Y: %.2f, Z: %.2f rads/s" % (icm.gyro))
#     print("Magnetometer X:%.2f, Y: %.2f, Z: %.2f uT" % (icm.magnetic))
    now = datetime.now()           
    file.write(str(now)+","+str(tmp117.temperature)+","+str(bme680.temperature)+","+str(bme680.gas)+","+str(bme680.relative_humidity)+","+str(bme680.pressure)+","+str(bme680.altitude)+","+str(icm.acceleration)+","+str(icm.gyro)+","+str(icm.magnetic)+","+cpu_temp()+","+str(ina.bus_voltage)+","+str(ina.current)+","+str(ina.power)+"\n")
    file.flush()
    i = i+1
    if (i == 500):
        camera.stop_recording()
        i = 0
        video_count += 1
        gigabytes_avail = psutil.disk_usage('/').free / 1024 / 1024 / 1024
        print("GB Available = %s" % gigabytes_avail)
        if (video_count == 5):
            break
        camera.start_recording('/home/pi/EOSS-317/testvideo%s.h264' % video_count)
    
    
#time.sleep(1)
#camera.stop_recording()
file.close()

