from machine import Pin, PWM, Timer, I2C

from Motor.Controller import Motor
from Receiver.ibusreceiver import IBusReceiver
from drivetrain import CalcWheelAmts
from MPU6050.imu import MPU6050

from math import sqrt,sin, atan2, radians
import utime
max_speed = 1
dt = 0.01
TranslationSplit = .5




        
def FadeStatus(t,l: PWM):
    amt=sin(t*32)/2+.5
    l.duty_u16(int(65535*amt))

CALIBRATION_TIME_SECONDS = 1
startCalTime = 0
def stopCalFunc():
    currentTime = utime.ticks_us()
    usecs = utime.ticks_diff(currentTime, startCalTime)
    dTime=(usecs/1000)/1000
    if dTime>CALIBRATION_TIME_SECONDS:
        return True
    else:
        return False



def main():

    statusLed=PWM(Pin(25,Pin.OUT))
    statusLed.duty_u16(65535)



    i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
    imu = MPU6050(i2c)

    global startCalTime, TranslationSplit
    startCalTime = utime.ticks_us()
    print("Starting IMU Calibration", startCalTime)
    imu.gyro.calibrate(stopCalFunc)
    print("Ending IMU Calibration")
    
    deltaZ=0
    heading=0
    
    UpTime=0
    dz = .1
    
    BRMotor = Motor(16,17,18, rev=True, deadzone = dz)
    FRMotor = Motor(19,20,21, deadzone = dz)
    FLMotor = Motor(26,27,22, rev=True, deadzone = dz)
    BLMotor = Motor(13,14,15, deadzone = dz)
    rx = IBusReceiver(10)
    #init to 0 until receiver gets non garbage data
    CalcWheelAmts(0,0,0,TranslationSplit)

    while True:
        startTime = utime.ticks_us()

        rx.ReadReceiver()
        if rx.ready == False:
            continue
        #Fade when ok
        FadeStatus(UpTime,statusLed)

        #Control Mode
        SW=rx.TwoPosSwitchChannel(6)
        if not SW:
            heading=0
            
        TranslationSplit = rx.MappedChannel(4,0.01,.999)
        
        #print(TranslationSplit)
        y = rx.MappedChannel(1,-1,1)
        x = rx.MappedChannel(0,-1,1)
        driveAngle = atan2(y,x)
        drivePower = sqrt(x*x+y*y)
        
        rot = rx.MappedChannel(3,-1,1)
        
        FLAmt, FRAmt, BLAmt, BRAmt = CalcWheelAmts(drivePower,driveAngle+radians(heading),-rot, TranslationSplit)
        #print(x,y)
        #print(heading)
        
        
        BRMotor.SetPercentOutput(BRAmt*max_speed)
        FRMotor.SetPercentOutput(FRAmt*max_speed)
        BLMotor.SetPercentOutput(BLAmt*max_speed)
        FLMotor.SetPercentOutput(FLAmt*max_speed)
    
    
        #Calculate the time of this loop iteration
        endTime = utime.ticks_us()
        usecs = utime.ticks_diff(endTime, startTime)
        dTime=(usecs/1000)/1000
        
        correctionfactor = 90/72
        deltaZ = -imu.gyro.z*dt   * correctionfactor
        heading+=deltaZ
        
        UpTime+=dTime
 
         #sleep desired - that time to make as close as possible to loop times of dt
        utime.sleep(dt-dTime)
        #utime.sleep(0.005)
   
if __name__ == '__main__':
    main()

