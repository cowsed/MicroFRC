from MPU6050.imu import MPU6050
from machine import Pin, I2C
import utime
from Receiver import receiver
from Servo import servo

#Gyroscope
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
imu = MPU6050(i2c)
dt = 0.01
heading  = 0

#ch1 - yaw - 14
#ch5 - sensitivity - 16
#ch6 - trim - 17
#Receiver
#rec = receiver.Receiver([14,16,17,18])

#serv = servo.Servo(19)

#Autopilot
desired_heading = 0
yawFactor = 1

sensitivity = .1
servoMaxOffFromCenter = 45



def clamp(l,h,v):
    if v<l:
        return l
    elif v>h:
        return h
    else:
        return v


print("Start Calibration")
imu.gyro.calibrate(stopCalFunc)
print("End Calibration")

frame = 0
while True:
    startTime = utime.ticks_us()
    #Update gyroscope
    dz = imu.gyro.z# + dzBias
    
    heading -= dz*dt
    print(heading)
    #if heading<0:
    #    heading+=360
    #heading = heading%360
    '''
    
    #Read receiver
    yawAmt = rec.MappedChannel(0,-1,1)
    desired_heading+=yawAmt*yawFactor  
    sensAmt = rec.MappedChannel(1,.1,.2)
    sensitivity = sensAmt

    trimAmt = rec.MappedChannel(2,-45,45)

    #calc autopilot
    servoAng = CalcControlAngle()
    #if frame%1==0:
    #    print(heading, desired_heading, servoAng)
    print(heading)
    serv.SetAngle(servoAng)
    '''
    endTime = utime.ticks_us()
    usecs = utime.ticks_diff(endTime, startTime)
    dTime=(usecs/1000)/1000
    utime.sleep(dt-dTime)
