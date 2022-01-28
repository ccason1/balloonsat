from gps3 import agps3
import time

# GPSDSocket creates a GPSD socket connection & request/retrieve GPSD output.
gps_socket = agps3.GPSDSocket()
# DataStream unpacks the streamed gpsd data into python dictionaries.
data_stream = agps3.DataStream()
gps_socket.connect()
gps_socket.watch()

for new_data in gps_socket:
    if new_data:
        data_stream.unpack(new_data)
        if data_stream.lon != 'n/a' and data_stream.lat != 'n/a' and data_stream.alt != 'n/a':
            print(data_stream.lon, data_stream.lat, data_stream.alt)
            print('--------------------------------')
 