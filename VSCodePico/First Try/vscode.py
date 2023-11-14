from machine import Pin, PWM
import utime
from math import sin

internalLEDController = PWM(Pin(25,Pin.OUT))

def clamp(l,h,v):
    if v<l:
        return l
    elif v>h:
        return h
    return h

def SetPercent(amt: float, dev: PWM) -> None:
    dev.duty_u16(int(clamp(0,1,amt)*65535))
    
time: float = 0
dt: float = .01
while True:
    amt = sin(time)/2+.5
    SetPercent(amt, internalLEDController)
    time+=dt
    utime.sleep(dt)


