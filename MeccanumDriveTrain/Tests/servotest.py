from machine import Pin, PWM
import utime

LOW = 1000000
MID = 1500000
HIGH = 2000000

s  = PWM(Pin(19))
s.freq(50)

print('l')
s.duty_ns(LOW)
utime.sleep(1)
print('n')
s.duty_ns(MID)
utime.sleep(1)
print('h')
s.duty_ns(HIGH)
utime.sleep(1)
