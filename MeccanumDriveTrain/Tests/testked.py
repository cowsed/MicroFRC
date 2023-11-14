# Example PIO to measure servo pulse width.
# produce a sample wave on GPIO 15
# measure pulse width on GPIO 16

import time
from machine import Pin, PWM
import rp2
import _thread

@rp2.asm_pio()
def pulsewidth():
    wrap_target()
    wait(1, pin, 0)                       # 0
    set(x, 0)                             # 1
    jmp(x_dec, "3")                       # 2
    label("3")
    jmp(x_dec, "4")                       # 3
    label("4")
    jmp(pin, "3")                         # 4
    mov(isr, x)                           # 5
    push(isr, block)                         # 6
    irq( 0)                         # 7
    wrap()

result = 0

baton = _thread.allocate_lock()
def handler(sm):
    global result
    # x-reg counts down
    value = 0x100000000 - sm.get()
    baton.acquire()               
    result = value  # 0.5 us resolution, so expect 2000 to 4000
                    #                       for    1ms  to 2ms
    baton.release()
    
pin16 = Pin(16, Pin.IN, Pin.PULL_UP)
sm0 = rp2.StateMachine(0, pulsewidth, freq=4_000_000, in_base=pin16, jmp_pin=pin16)
sm0.irq(handler)
sm0.active(1)

print("measure pulse width on pin 16")

# Set the PWM frequency, servo use 50 Hz.
#pwm.freq(50)

ms_1 = 3277 # one millisecond 65535/20
ms_2 = 6553 # two millisecond
pulse_width = ms_1
    

led = Pin(25, Pin.OUT)
while True:
    led.toggle() # activity indication
    
    baton.acquire()
    r = result
    baton.release()
    print(r)

    
    time.sleep(0.1)