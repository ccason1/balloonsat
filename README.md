# Setup procedure

## 1. Micro SD card image

1. Latest Raspbian.
2. 3 partitions:
   1. OS.
   2. Telemetry.
   3. Camera data (stills, videos).
3. Libraries:
   1. Sensor libraries
      | Sensor | Installation | Reference URL | Guide |
      | --- | --- | --- | --- |
      | CircuitPython | `sudo pip3 install Adafruit-Blinka` | https://github.com/adafruit/Adafruit_Blinka | https://learn.adafruit.com/circuitpython-on-raspberrypi-linux |
      | High-accuracy temperature | `sudo pip3 install adafruit-circuitpython-tmp117` | https://github.com/adafruit/Adafruit_CircuitPython_TMP117 | https://learn.adafruit.com/adafruit-tmp117-high-accuracy-i2c-temperature-monitor/python-circuitpython |
      | Enrironmental | `sudo pip3 install adafruit-circuitpython-bme680` | https://github.com/adafruit/Adafruit_CircuitPython_BME680 | https://learn.adafruit.com/adafruit-bme680-humidity-temperature-barometic-pressure-voc-gas/python-circuitpython |
      | IMU | `sudo pip3 install adafruit-circuitpython-icm20x` | https://github.com/adafruit/Adafruit_CircuitPython_ICM20X | https://learn.adafruit.com/adafruit-tdk-invensense-icm-20948-9-dof-imu/python-circuitpython |
      | Voltage and current | `sudo pip3 install adafruit-circuitpython-ina219` | https://github.com/adafruit/Adafruit_CircuitPython_INA219 | https://learn.adafruit.com/adafruit-ina219-current-sensor-breakout/python-circuitpython |
   3. RockBLOCK libraries.
   4. GPS libraries.
   5. Camera?
   6. UPS library.
4. Drivers:
   1. Camera.
5. Configuration:
   1. Adafruit script includes a lot of setup for the RPi.
   2. I2C enable.
   3. Camera enable.
   4. Serial enable.
6. Transfer (R/W) between Micro SD and other storage.

## 2. Run ground test

Tests if the image has everything set up correctly, including all the components.

## 3. Flight executive test

1. v0.1: Startup on power on, test power, and shutdown.
2. 
