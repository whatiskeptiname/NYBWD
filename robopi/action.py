import RPi.GPIO as IO 
import time
import math
import serial    #install pyserial instate serial package  
import py_qmc5883l  
import global_var       


ma0 = 18
ma1 = 23
mb0 = 24
mb1 = 25
pwm_a = 8
pwm_b = 7      
trigger = 27
echo = 17        
servo = 12               

IO.setwarnings(False)
IO.cleanup()
IO.setmode(IO.BCM)
IO.setup(ma0, IO.OUT)
IO.setup(ma1, IO.OUT)
IO.setup(mb0, IO.OUT)
IO.setup(mb1, IO.OUT)
IO.setup(pwm_a, IO.OUT)
IO.setup(pwm_b, IO.OUT)
IO.setup(trigger, IO.OUT)
IO.setup(echo, IO.OUT)
IO.setup(servo, IO.OUT)
        
IO.output(ma0, 0)
IO.output(ma1, 0)
IO.output(mb0, 0)
IO.output(mb1, 0)

pa = IO.PWM(pwm_a, 50)
pb = IO.PWM(pwm_b, 50)
 

class Action:

    def left(self, speed):
        IO.output(ma0, 1)
        IO.output(ma1, 0)
        IO.output(mb0, 0)
        IO.output(mb1, 1)
        pa.start(speed)
        pb.start(speed)
             
    def forward(self, speed):
        IO.output(ma0, 0)
        IO.output(ma1, 1)
        IO.output(mb0, 0)
        IO.output(mb1, 1)   
        pa.start(speed)
        pb.start(speed)   

    def right(self, speed):
        IO.output(ma0, 0)
        IO.output(ma1, 1)
        IO.output(mb0, 1)
        IO.output(mb1, 0)
        pa.start(speed)
        pb.start(speed)

    def backward(self, speed):
        IO.output(ma0, 1)
        IO.output(ma1, 0)
        IO.output(mb0, 1)
        IO.output(mb1, 0)
        pa.start(speed)
        pb.start(speed)

    def stop(self):
        IO.output(ma0, 0)
        IO.output(ma1, 0)
        IO.output(mb0, 0)
        IO.output(mb1, 0)
        pa.stop()
        pb.stop()

    def auto_forward(self, speed, itration):
        global_var.i_length = 0
        while True:
            proximity = self.proximity()
            if proximity > 35 :
                print(global_var.i_breadth, global_var.i_length)
                self.forward(speed)
                time.sleep(0.01)
                global_var.i_length = global_var.i_length + 1
                if global_var.i_length >= itration:
                    self.stop()
                    break
            else:
                self.stop()

    def auto_forward_short(self, speed, itration):
        i = 0
        while True:
            proximity = self.proximity()
            if proximity > 35 :
                print(global_var.i_breadth, global_var.i_length, "short movement")
                self.forward(speed)
                time.sleep(0.01)
                i = i + 1 
                if i >= itration:
                    global_var.i_length = 0
                    global_var.i_breadth = global_var.i_breadth + 1
                    self.stop()
                    break
            else:
                self.stop()

    def proximity(self):
        #min 0.00017976760864257812
        #max 0.004200458526611328
        while True:
            IO.output(trigger, 1)
            time.sleep(0.00001)
            IO.output(trigger, 0)
            StartTime = time.time()
            StopTime = time.time()
            while IO.input(echo) == 0:
                StartTime = time.time()
            while IO.input(echo) == 1:
                StopTime = time.time()
            TimeElapsed = StopTime - StartTime
            if TimeElapsed > 0.004200458526611328:
                return 100
                continue
            distance = (TimeElapsed * 34300) / 2
            return distance
            break

    def position(self):
        global NMEA_buff
        gpgga_info = "$GPGGA,"
        ser = serial.Serial ("/dev/ttyS0")    
        GPGGA_buffer = 0
        NMEA_buff = 0
        return 27.698540494362685, 85.29501488465684
        # while True:
        #     received_data = (str)(ser.readline())                   
        #     GPGGA_data_available = received_data.find(gpgga_info)                    
        #     if(GPGGA_data_available>0):
        #         GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  
        #         NMEA_buff = (GPGGA_buffer.split(','))                              
        #         nmea_latitude = NMEA_buff[1]            
        #         nmea_longitude = NMEA_buff[3]           
        #         lat = float(nmea_latitude)/100.00
        #         degrees = int(lat)
        #         mm_mmmm = (lat - int(lat))/0.6
        #         position = degrees + mm_mmmm
        #         lat = "%.15f" %(position)
        #         longi = float(nmea_longitude)/100.00
        #         degrees = int(longi)
        #         mm_mmmm = (longi - int(longi))/0.6
        #         position = degrees + mm_mmmm
        #         longi = "%.15f" %(position)
        #         return lat, longi

    def positionBearing(self):
        sensor = py_qmc5883l.QMC5883L()
        bposn = sensor.get_bearing()
        return bposn

    def destinationBearing(self,lat1, long1, lat2, long2):
        dLon = (long2 - long1)
        y = math.sin(dLon) * math.cos(lat2)
        x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dLon)
        brng = math.atan2(y, x)
        brng = math.degrees(brng)
        brng = (brng + 360) % 360
        bdest = 360 - brng # count degrees clockwise - remove to make counter-clockwise
        return bdest

    def turnAngle(self, bposn, bdest ):
        brotation = bdest - bposn
        if brotation< -180: 
            brotation = brotation + 360
        if brotation > 180:
            brotation = brotation - 360
        return brotation

    def turn(self, turn_angle, speed):
        if turn_angle > 0 :
            while True:
                initial_bposn = self.positionBearing()
                if initial_bposn != None:
                    break 
            turned_angle = 0
            while True:
                self.right(speed)
                current_bposn = self.positionBearing()
                if current_bposn == None:
                    self.stop()
                    continue
                turned_angle = abs(initial_bposn - current_bposn)
                if turned_angle >= turn_angle:
                    self.stop()
                    break

        if turn_angle < 0:
            while True:
                initial_bposn = self.positionBearing()
                if initial_bposn != None:
                    break 
            while True:
                self.left(speed)
                current_bposn = self.positionBearing()
                if current_bposn == None:
                    self.stop()
                    continue
                turned_angle = abs(initial_bposn - current_bposn)
                if turned_angle >= abs(turn_angle):
                    self.stop()
                    break

    def arm(self, angle):
        if(angle > 0 and angle < 181):
            angle = angle/180*12
            ps = IO.PWM(servo, 50)
            ps.start(angle)
            time.sleep(1)
            ps.stop()
        else:
            ps.stop()
            