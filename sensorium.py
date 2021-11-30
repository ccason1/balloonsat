#Sensor class to encapsulate all sensors for the MSUSAT project
#Each specific sensor has its own behavior and is represented in a unique subclass

import psutil
import adafruit_tmp117
import board
import adafruit_rockblock
import time
import adafruit_bme680
import adafruit_icm20x


def setPort(port):
    global PORT
    if(true):
        PORT = port
        return 0
    else:
        return -1
    

#return a properly delineated string from input sensor data
def Delineate(senses):

    sensation = ""

    for sense in senses:
        
        sensation += str(sense) + ","

    return sensation


class Sensor:
    
    def __init__(self, addy, sensorType, port):
        
        self.addy = addy
        self.port = port
        self.sensorType = sensorType
        self.i2c = board.I2C()
        

    def sense():
        pass
    

    def record():
        pass


class Internal(Sensor):

    def __init__(self, port = PORT):
        
        super("INTERNAL", "Internal", port)
        self.cpuTemp = 0
        self.cpuUsage = 0
        self.memUsage = 0
        self.diskUsage = 0
        

    def sense():
        
        self.cpuTemp = psutil.sensors_temperatures()['cpu_thermal'][0][1]
        self.cpuUsage = psutil.cpu_percent()
        self.memUsage = psutil.virtual_memory()[2]
        self.diskUsage = psutil.disk_usage('/')[3]
        

    def record():
        
        return Delineate([self.cpuTemp, self.cpuUsage, self.memUsage, self.diskUsage])


class TMP117(Sensor):

    def __init__(self, addy = "0x48", port = PORT):
        
        super(addy, "Temperature", port)
        self.envTemp = 0
        self.hi = False
        self.lo = False
        

    def sense():
        
        self.envTemp = adafruit_tmp117.TMP117(self.i2c).temperature
        self.hi = adafruit_tmp117.TMP117(self.i2c).alert_status.high_alert
        self.lo = adafruit_tmp117.TMP117(self.i2c).alert_status.low_alert

    
    def record():
        
        return Delineate([self.envTemp, self.hi, self.lo])


    def setHi(hi):
        
        adafruit_tmp117.TMP117(self.i2c).high_limit = hi


    def setLo(lo):
        
        adafruit_tmp117.TMP117(self.i2c).low_limit = lo


class MAXM8Q(Sensor):

    def __init__(self, addy, port = PORT):
        
        super(addy, "GPS", port)


class BerryGPS(Sensor):

    def __init__(self, default = True, port = PORT):
        
        if default:
            
            super("0x1C", "GPS", port)
            
        else:
            
            super("0x1E", "GPS", port)


class BME680(Sensor):

    def __init__(self, default = True, port = PORT):

        if default:
            
            super("0x77", "Gas/Temperature", port)
            
        else:
            
            super("0x76", "Gas/Temperature", port)

        self.temperature = 0
        self.gas = 0
        self.humid = 0
        self.pressure = 0
        self.altitude = 0


    def sense():
        bme = adafruit_bme680.Adafruit_BME680_I2C(self.i2c)
        
        self.temperature = bme.temperature
        self.gas = bme.gas
        self.humid = bme.relative_humidity
        self.pressure = bme.pressure
        self.altitude = bme.altitude


    def record():
        return Delineate([self.temperature, self.gas, self.humid, self.pressure, self.altitude])


class ICM20948(Sensor):

    def __init__(self, default = True, port = PORT):

        if default:
            
            super("0x69", "Motion", port)
            
        else:
            
            super("0x68", "Motion", port)

        self.accelX = 0
        self.accelY = 0
        self.accelZ = 0
        self.gyroX = 0
        self.gyroY = 0
        self.gyroZ = 0
        self.magX = 0
        self.magY = 0
        self.magZ = 0


    def sense():
        icm = adafruit_icm20x.ICM20948(self.i2c)
        accel = icm.acceleration
        gyro = icm.gyro
        mag = icm.magnetic

        self.accelX = accel[0]
        self.accelY = accel[1]
        self.accelZ = accel[2]
        self.gyroX = gyro[0]
        self.gyroY = gyro[1]
        self.gyroZ = gyro[2]
        self.magX = mag[0]
        self.magY = mag[1]
        self.magZ = mag[2]


    def record():
        return Delineate([self.accelX, self.accelY, self.accelZ, self.gyroX, self.gyroY, self.gyroZ, self.magX, self.magY, self.magZ])


class EP0136(Sensor):

    def __init__(self, addy, port = PORT):
        
        super(addy, "Power", port)
