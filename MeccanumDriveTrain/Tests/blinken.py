import utime
from machine import Pin, PWM
import rp2

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def blink():
    wrap_target()
    set(pins, 1)   [31]
    nop()          [31]
    nop()          [31]
    nop()          [31]
    nop()          [31]
    nop()          [31]
    nop()          [31]
    set(pins, 0)   [31]
    nop()          [31]
    nop()          [31]
    nop()          [31]
    nop()          [31]
    nop()          [31]
    nop()          [31]
    wrap()
 
#p = Pin(15, Pin.OUT)
#p.on()
sm = rp2.StateMachine(1, blink, freq=3000, set_base=Pin(15))
sm2 = rp2.StateMachine(0, blink, freq=2000, set_base=Pin(25))

# Run the state machine for 3 seconds.  The LED should blink.
sm.active(1)
sm2.active(1)
utime.sleep(3)
sm.active(0)
sm2.active(0)
