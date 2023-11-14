# Example PIO to measure servo pulse width.

#https://forums.raspberrypi.com/viewtopic.php?t=309969
import time
from machine import Pin, PWM
import rp2
import _thread

def normal(v, mn,mx):
    return (v-mn)/(mx-mn)

@rp2.asm_pio()
def pulsewidth0():
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
@rp2.asm_pio()
def pulsewidth1():
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
    irq( 1)                         # 7
    wrap()
@rp2.asm_pio()
def pulsewidth2():
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
    irq( 2)                         # 7
    wrap()
@rp2.asm_pio()
def pulsewidth3():
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
    irq( 3)                         # 7
    wrap()


PIOProgs = [pulsewidth0,pulsewidth1,pulsewidth2,pulsewidth3]
result = [0,1,2,3]

baton = _thread.allocate_lock()
def handler(sm, index):
    global result
    # x-reg counts down
    value = 0x100000000 - sm.get()
    baton.acquire()               
    result[index] = value  # 0.5 us resolution, so expect 2000 to 4000
                    #                       for    1ms  to 2ms
    baton.release()
                    #                       for    1ms  to 2ms
    

pin16 = Pin(16, Pin.IN, Pin.PULL_UP)
sm0 = rp2.StateMachine(0, PIOProgs[0], freq=4_000_000, in_base=pin16, jmp_pin=pin16)
sm0.irq(lambda sm: handler(sm,0))


pin17 = Pin(17, Pin.IN, Pin.PULL_UP)
sm1 = rp2.StateMachine(1, PIOProgs[1], freq=4_000_000, in_base=pin17, jmp_pin=pin17)
sm1.irq(lambda sm: handler(sm,1))

pin18 = Pin(18, Pin.IN, Pin.PULL_UP)
sm2 = rp2.StateMachine(2, PIOProgs[2], freq=4_000_000, in_base=pin18, jmp_pin=pin18)
sm2.irq(lambda sm: handler(sm,2))

pin14 = Pin(14, Pin.IN, Pin.PULL_UP)
sm3 = rp2.StateMachine(3, PIOProgs[3], freq=4_000_000, in_base=pin14, jmp_pin=pin14)
sm3.irq(lambda sm: handler(sm,3))

sm0.active(1)
sm1.active(1)
sm2.active(1)
sm3.active(1)


pwmax = 4000
pwmin = 2000
    

led = Pin(25, Pin.OUT)
ac = PWM(led)
ac2 = PWM(Pin(15,Pin.OUT))

while True:
    #led.toggle() # activity indication
    
    baton.acquire()
    r1 = result[0]
    r2 = result[1]
    r3 = result[2]
    r4 = result[3]
    
    baton.release()
    

    print(r1,r2,r3,r4)
    #print(sm0.irq(), sm1.active())
    
    amt = (normal(r1,pwmin,pwmax))
    ac.duty_u16(int(amt*65535))
    amt2 = (normal(r2,pwmin,pwmax))
    ac2.duty_u16(int(amt2*65535))

    time.sleep(0.1)