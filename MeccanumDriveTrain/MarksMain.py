from MicroFRC.Recievers.pwmreceiver import PWMReceiver
from MicroFRC.Motors.Controller import Motor
import utime


FLMotor = Motor(11, 10, 9, rev = False, deadzone = 0.15) #In, In, PWM, 
FRMotor = Motor(19, 20, 21, rev = True, deadzone = 0.15)
RLMotor = Motor(16, 17, 18, rev = True, deadzone = 0.15)
RRMotor = Motor(13, 14, 12, rev = True, deadzone = 0.15)

transVentralSpd = [0, 0, 0, 0]
transCrabwiseSpd = [0, 0, 0, 0]
revolveSpd = [0, 0, 0, 0]

aggregateSpd = [0, 0, 0, 0]

rx = PWMReceiver([22, 26, 27, 28])
correction = 5/3.0

def clamp(val, limit):
    if val > limit:
        val = limit
    elif val < -limit:
        val = -limit
    return val

def translateFore(speed):
    global transVentralSpd
    transVentralSpd[0] = speed
    transVentralSpd[1] = speed
    transVentralSpd[2] = speed
    transVentralSpd[3] = speed
    
def translateCrabwise(speed):
    transCrabwiseSpd[0] = speed
    transCrabwiseSpd[1] = -speed
    transCrabwiseSpd[2] = -speed
    transCrabwiseSpd[3] = speed
    
def revolve(speed):
    revolveSpd[0] = speed
    revolveSpd[1] = -speed
    revolveSpd[2] = speed
    revolveSpd[3] = -speed
    
    
def amalgamate(transVentral, transCrabwise, revolve):
        aggregate = [0, 0, 0, 0]
        for i in range(4):
            aggregate[i] = transVentral[i] + transCrabwise[i] + revolve[i]
        return aggregate

def rescale(speeds):
    maxSpd = max(speeds)
    if maxSpd > 1:
        for i in range(4):
            speeds[i] = speeds[i]/maxSpd
    

while True:
    ch1 = rx.MappedChannel(0, -correction, correction)
    ch2= rx.MappedChannel(1, correction, -correction)
    ch3 = rx.MappedChannel(2, -correction, correction)
    ch4 = rx.MappedChannel(3, -1/.815, 1/.815)
    
    ch2 = clamp(ch2, 1)
    ch3 = clamp(ch3, 1)
    ch1 = clamp(ch1, 1)
    
    translateFore(ch2)
    translateCrabwise(ch3)
    revolve(ch1)
    
    aggregateSpd = amalgamate(transVentralSpd, transCrabwiseSpd, revolveSpd)
    rescale(aggregateSpd)
    
    FLMotor.SetPercentOutput(aggregateSpd[0])
    FRMotor.SetPercentOutput(aggregateSpd[1])
    RLMotor.SetPercentOutput(aggregateSpd[2])
    RRMotor.SetPercentOutput(aggregateSpd[3])
    
    #print(aggregateSpd)
    #utime.sleep(0.1)



