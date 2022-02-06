import serial
import time

ser = serial.Serial('/dev/ttyS0',9600,timeout=10)

# command to set module to flight/nav mode
# header = xB5 x62
# class = x06
# id = x24
# x24 x00 is little endian 2 byte length of UBX message payload
# xFF xFF bitmask
# x06 for airborne with < 1g
# x00 default settings for the rest of the payload
# last two bytes are the CRC checksums calculated by u-center
cmd_navmode = b'\xB5\x62\x06\x24\x24\x00\xFF\xFF\x06\x03\x00\x00\x00\x00\x10\x27\x00\x00\x05\x00\xFA\x00\xFA\x00\x64\x00\x5E\x01\x00\x3C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x84\x08'

# poll for NAV5
cmd_poll_navmode = b'\xB5\x62\x06\x24\x00\x00\x2A\x84'

if True == ser.is_open:
    ser.write(cmd_navmode)
    
    ser.write(cmd_poll_navmode)
    
    # skim through receiver input until we reach the NAV5 confirmation
    nmea = ser.read_until(b'\xB5\x62\x06\x24\x24\x00\xFF\xFF')
    
    # read the first byte of the payload, which is the current navModel (navigation engine dynamic platform model)
    # (i.e. whether it's in flight mode or not)
    dyn_model_byte = ser.read()
    
    # byte that means its in airborne with < 1g mode
    # i.e. flight mode, the one we want
    airborne_less_than_1g = b'\x06'
    
    print("dynModel byte = " + str(dyn_model_byte))
    if dyn_model_byte == airborne_less_than_1g:
        print("Navigation mode set successfully.")
    else:
        print("Navigation mode not correct.")
        print("Location accuracy may be reduced.")
        
    time.sleep(1)
    ser.close()