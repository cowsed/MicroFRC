from machine import Pin, PWM

p = PWM(Pin(16, Pin.IN))
p.freq(50)
while(1):
    print(p.duty_u16(Pin.IN, Pin.PULL_UP))