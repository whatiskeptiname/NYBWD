import serial               #import serial pacakge
from time import sleep        #import package for opening link in browser
import sys  
#sudo To enable permission for the port
# sudo chmod a+rw /dev/ttyS0


global NMEA_buff
global lat_in_degrees
global long_in_degrees
gpgga_info = "$GPGGA,"
ser = serial.Serial ("/dev/ttyS0")              #Open port with baud rate
GPGGA_buffer = 0
NMEA_buff = 0
lat_in_degrees = 0
long_in_degrees = 0
i = 0
while True:
    received_data = (str)(ser.readline())                   
    GPGGA_data_available = received_data.find(gpgga_info)                    
    if (GPGGA_data_available>0):
        GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  
        NMEA_buff = (GPGGA_buffer.split(','))              
        # nmea_time = []
        # nmea_latitude = []
        # nmea_longitude = []
        nmea_time = NMEA_buff[0]                
        nmea_latitude = NMEA_buff[1]            
        nmea_longitude = NMEA_buff[3]           
        lat = float(nmea_latitude)/100.00
        degrees = int(lat)
        mm_mmmm = (lat - int(lat))/0.6
        position = degrees + mm_mmmm
        lat = "%.15f" %(position)
        longi = float(nmea_longitude)/100.00
        degrees = int(longi)
        mm_mmmm = (longi - int(longi))/0.6
        position = degrees + mm_mmmm
        longi = "%.15f" %(position)
        print("NMEA Time: ", nmea_time)
        print (lat, longi)
        print("_______________________________________")


# import serial
# import time
# import string 
# import pynmea2
# while True: 
#     port = "/dev/ttyS0"
#     ser=serial.Serial(port,baudrate=9600,timeout=0.5)
#     dataout =pynmea2.NMEAStreamReader()
#     newdata=ser.readline()
#     # print(newdata)

#     if newdata[0:6] == "$GPRMC":
#         newmsg=pynmea2.parse(newdata)
#         lat=newmsg.latitude
#         lng=newmsg.longitude
#         gps="Latitude=" +str(lat) + "and Longitude=" +str(lng)
#         print(gps)

# #!/usr/bin/python3
# from gps3 import agps3
# gps_socket = agps3.GPSDSocket()
# data_stream = agps3.DataStream()
# gps_socket.connect()
# gps_socket.watch()
# for new_data in gps_socket:
#     if new_data:
#         data_stream.unpack(new_data)
#         print('Altitude = ', data_stream.alt)
#         print('Latitude = ', data_stream.lat)
#         print('Longitude = ', data_stream.lon)