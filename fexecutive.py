from subprocess import run

# 1. all necessary imports
# TODO: What is imported for what, in EOL comments
import sys
import smbus
import struct
import RPi.GPIO as GPIO
import time
import os
from subprocess import run
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
import serial
from adafruit_rockblock import RockBlock
from gps3 import agps3   # GPS library

# 2. setup all components
GPIO_PORT = 26          # psu
I2C_ADDR = 0x36         # psu

bus = smbus.SMBus(1)    # psu

TELEMETRY_FILENAME = "/home/pi/flight_telemetry/telemetry_log.csv"
telemetry_file =open(TELEMETRY_FILENAME,"a")

i2c = board.I2C()  # uses board.SCL and board.SDA

bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)
tmp117 = adafruit_tmp117.TMP117(i2c)
icm = adafruit_icm20x.ICM20948(i2c)
ina = INA219(i2c)

uart = serial.Serial("/dev/ttyUSB0", 19200)   # ttyUSBx has to be checked
rb = RockBlock(uart)

# GPS Setup Start <====================
# GPSDSocket creates a GPSD socket connection & request-retrieves the GPSD output
gps_socket = agps3.GPSDSocket()

# DataStream unpacks the streamed GPSD data into Python dictionaries
data_stream = agps3.DataStream()
gps_socket.connect()
gps_socket.watch()

gps_lat = -360.0
gps_lon = -360.0
gps_alt = -100.0
# GPS Setup End <====================

bme680.sea_level_pressure = 1013.25
temperature_offset = -5

def read_voltage(bus):
    address = I2C_ADDR
    read = bus.read_word_data(address, 2)
    swapped = struct.unpack("<H", struct.pack(">H", read))[0]
    voltage = swapped * 1.25 /1000 /16
    return voltage

def read_capacity(bus):
    address = I2C_ADDR
    read = bus.read_word_data(address, 4)
    swapped = struct.unpack("<H", struct.pack(">H", read))[0]
    capacity = swapped /256
    return capacity


def cpu_temp():
    temp = os.popen("vcgencmd measure_temp").readline()
    temp = temp.replace("'C","")
    temp = temp.replace("\n","")
    return (temp.replace("temp=",""))

# header line for telemetry file
if os.stat(TELEMETRY_FILENAME).st_size == 0:
    telemetry_file.write("date_time," +
                        "gps_lon,gps_lat,gps_alt,tmp117_temp_out," + 
                        "bme680_temp_in,bme680_gas,bme680_rel_hum,bme680_press,bme680_alt" +
                        "icm_acc_x,icm_acc_y,icm_acc_z," +
                        "icm_gyro_x,icm_gyro_y,icm_gyro_z," +
                        "icm_magn_x,icm_magn_y,icm_magn_z," +
                        "ina_bus_vol,ina_bus_cur,ina_bus_pow," +
                        "ups_vol,ups_cap," +
                        "temp_cpu\n")

# 3. start wifi hot spot and streaming as a separate process
#       systemctl enable hostapd 
#       systemctl enable dnsmasq

# 4. main loop running with some delay after last iteration
shut_down = False
once_in_every_n_lines = 35       # number of telemetry loops between rockblock send
telemetry_line_counter = 0       # telemetry loop counter
while True:
    # check for low voltage
    psu_voltage = read_voltage(bus)
    print("Voltage: ", psu_voltage)
    psu_capacity = read_capacity(bus)
    print("Capacity: ", psu_capacity)
    if psu_voltage < 3.00 or psu_capacity < 20:
        msg = "Battery low (vol<3.00V or cap<20%) vol=" + str(psu_voltage) + " cap=" + str(psu_capacity)
        telemetry_file.write(msg)
        print(msg)
        shut_down = True
        break

    # get timestamp w/o microseconds
    now = datetime.now()
    now = now.replace(microsecond=0)  # truncate ms
    now.strftime('%y-%m-%d %H:%M:&S')
    # print(now)

    # get GPS coordinates
    for new_data in gps_socket:
        if new_data:
            data_stream.unpack(new_data)
            if data_stream.lon != 'n/a' and data_stream.lat != 'n/a' \
                and data_stream.alt != 'n/a':
                gps_lon = data_stream.lon
                gps_lat = data_stream.lat
                gps_alt = data_stream.alt
                break

    # get sensor data points
    data_points = [tmp117.temperature, 
        bme680.temperature, bme680.gas, bme680.relative_humidity, bme680.pressure, bme680.altitude, 
        *icm.acceleration, *icm.gyro, *icm.magnetic, 
        ina.bus_voltage, ina.current, ina.power,
        psu_voltage, psu_capacity]

    # truncate to 2 decimal places
    as_string = ','.join([str(round(d, 2)) for d in data_points])

    # compose data line
    line = str(now) + ',' + \
        str(gps_lon) + ',' + str(gps_lat) + ',' + str(gps_alt) + ',' + \
        as_string + ',' + \
        cpu_temp() + '\n'
    print(len(line))  # 126 w/ tmp117

    # append line to telemetry file
    telemetry_file.write(line)
    telemetry_file.flush()

    # send line of telemetry over iridium rockblock
    if telemetry_line_counter % once_in_every_n_lines == 0:

        rb.data_out = str.encode(line)
        # rb.text_out = line   # library hacked (TODO: revert)
        print("Attempting to send telemetry over Iridium...")
        status = rb.satellite_transfer()
        
        # loop as needed
        retry = 2
        while status[0] > 8 and retry > 0:
            time.sleep(10)
            status = rb.satellite_transfer()
            print("Retrying", retry, status)
            retry -= 1

        if status[0] > 8:
            print("Unsuccessful. Aborting!")
        else:
            print("Success. DONE!")

    telemetry_line_counter += 1

# close telemetry file
telemetry_file.close()

# close GPS socket
gps_socket.close()

# shut down
if shut_down:
    print("Shutting down in 60 sec")
    run("shutdown --poweroff 1", shell=True)
else:
    print("Not shutting down. Exiting...")