from gps3 import agps3
import os
from datetime import datetime

GPS_FILENAME = "/home/pi/flight_telemetry/gps_log.csv"
telemetry_file =open(GPS_FILENAME,"a")

if os.stat(GPS_FILENAME).st_size == 0:
    telemetry_file.write("date_time," +
                        "gps_lon,gps_lat,gps_alt\n")


# GPSDSocket creates a GPSD socket connection & request/retrieve GPSD output.
gps_socket = agps3.GPSDSocket()
# DataStream unpacks the streamed gpsd data into python dictionaries.
data_stream = agps3.DataStream()
gps_socket.connect()
gps_socket.watch()

try:
    for new_data in gps_socket:
        if new_data:
            data_stream.unpack(new_data)
            now = datetime.now()
            now = now.replace(microsecond=0)  # truncate ms
            now.strftime('%y-%m-%d %H:%M:&S')
            line = now + str(data_stream.lon) + "," + \
                str(data_stream.lat) + "," + str(data_stream.alt) + "\n"
            telemetry_file.write(line)
            telemetry_file.flush()
except KeyboardInterrupt:
    telemetry_file.close()
