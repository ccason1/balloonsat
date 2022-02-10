# Information About flightmode.py

## References
[Protocol Manual](https://www.u-blox.com/sites/default/files/products/documents/u-blox8-M8_ReceiverDescrProtSpec_UBX-13003221.pdf)  
Page 169: A diagram of the UBX command frame structure.  
Page 217: Information regarding the specific hex code in the command to set the receiver to airborne mode.  

Checksums and default commands from the u-center software package.  

## Supported Models and Versions
To find the protocol version of your receiver, refer to page 1 of the protocol manual.  

### Supported Models
(space-separated)  
CAM-M8C CAM-M8Q EVA-M8M EVA-M8M EVA-M8Q MAX-M8C MAX-M8Q MAX-M8W NEO-M8M NEO-M8N NEO-M8Q NEO-M8Q NEO-M8J LEA-M8S SAM-M8Q ZOE-M8G ZOE-M8Q ZOE-M8B EVA-8M MAX-8C MAX-8Q UBX-13003221 NEO-8Q NEO-M8P NEO-M8P NEO-M8P NEO-M8P NEO-M8L NEO-M8L NEO-M8L NEO-M8L NEO-M8L NEO-M8L NEO-M8L NEO-M8L NEO-M8L EVA-M8E NEO-M8U NEO-M8U NEO-M8U NEO-M8U NEO-M8T LEA-M8T LEA-M8T LEA-M8F

### Supported Protocol Versions
u-blox / u-blox M8 protocol versions:  
(space-separated)  
15 15.01 16 17 18 19 19.1 19.2 20 20.01 20.1 20.2 20.3 22 22.01 23 23.01

## Available Dynamic Platform Models
0: portable  
2: stationary  
3: pedestrian  
4: automotive  
5: sea  
6: airborne with <1g acceleration  
7: airborne with <2g acceleration  
8: airborne with <4g acceleration  
9: wrist-worn watch (not supported in protocol versions less than 18)  
10: motorbike (supported in protocol versions 19.2, and 35.10)  
11: robotic lawn mower  
12: electric kick scooter  

## Persistence of Settings
The following information comes from tests run on a MAX-M8Q with protocol version 18.

### Power Cycling
After shutting down the Raspberry Pi and removing power, then powering back up, the mode defaults to 0: portable.

### Soft Reboot
After rebooting the Raspberry Pi without removing power, whatever setting it was on from before the reboot remains.

### Time Interval
I have not found anything in the protocol about whether or not the dynamic platform model is reset after a period of time without power cycling. When I tested this, the setting did not change after 1.5 hours.
