import serial
import time

ser = serial.Serial('/dev/ttyS0', 9600, timeout=5)

# command to set module to flight/nav mode
# header = xB5 x62
# class = x06
# id = x24
# x24 x00 is little endian 2 byte length of UBX message payload
# xFF xFF bitmask
# x06 for airborne with < 1g
# default settings for the rest of the payload
# last two bytes are the CRC checksums calculated by u-center
cmd_navmode = b'\xB5\x62\x06\x24\x24\x00\xFF\xFF\x06\x03\x00\x00\x00\x00\x10\x27\x00\x00\x05\x00\xFA\x00\xFA\x00\x64\x00\x5E\x01\x00\x3C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x84\x08'

# command to poll for NAV5
cmd_poll_navmode = b'\xB5\x62\x06\x24\x00\x00\x2A\x84'

def set_to_flight_mode():
    """Sets the u-blox M8 receiver's dynamic platform model to airborn with < 1g"""
    
    if ser.is_open:
    
        ser.write(cmd_navmode)
            
        time.sleep(1)
        ser.close()
    
    
def verify_in_flight_mode():
    """Returns True if the u-blox M8 receiver's dynamic platform model is set to airborne with < 1g"""
    
    if ser.is_open:
    
        ser.write(cmd_poll_navmode)
        
        # skim through receiver input until we reach the NAV5 confirmation
        nmea = ser.read_until(b'\xB5\x62\x06\x24\x24\x00\xFF\xFF')
        
        # read the first byte of the payload, which is the current navModel (navigation engine dynamic platform model)
        # (i.e. whether it's in flight mode or not)
        dyn_model_byte = ser.read()
        
        # byte that means its in airborne with < 1g mode
        # i.e. flight mode, the one we want
        airborne_less_than_1g = b'\x06'
        
        if dyn_model_byte == airborne_less_than_1g:
            # navigation mode set successfully
            return True
        else:
            # navigation mode not correct
            # location accuracy may be reduced
            return False