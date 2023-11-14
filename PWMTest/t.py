from machine import PWM, Pin, Timer
import time
lastPWMRead=0

def ReadPWM():
    print(lastPWMRead)

pin = Pin(0)

pwm = PWM(pin)          # create a PWM object on a pin
#pwm.duty_u16(32768)     # set duty to 50%

# reinitialise with a period of 200us, duty of 5us
#pwm.init(freq=5000, duty_ns=5000)

##pwm.duty_ns(3000)       # set pulse width to 3us

while True:
    ReadPWM()
    time.sleep(.5)


pwm.deinit()