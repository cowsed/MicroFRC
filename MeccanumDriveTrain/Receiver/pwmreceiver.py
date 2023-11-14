from machine import Pin
import rp2
import _thread
def normal(v, mn,mx):
    return ((v-mn)/(mx-mn))
def mapFromNormalized(v, mn,mx):
    return v*(mx-mn)+mn

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

def normalize(v, mn,mx):
    return (v-mn)/(mx-mn)

PIOProgs = [pulsewidth0,pulsewidth1,pulsewidth2,pulsewidth3]

baton = _thread.allocate_lock()

def handler(sm, results,resultNorms, index):
    # x-reg counts down
    value = 0x100000000 - sm.get()
    baton.acquire()               
    results[index] = value 
    resultNorms[index] = normalize(value,2000,4000) 
    baton.release()



class PWMReceiver:
    resultsNorm = [0,0,0,0]
    results = [0,1,2,3]
    pins = [0,1,2,3]
    statemachines = [0,1,2,3]
    
    def __init__(self, channelPins):
        if len(channelPins)>4:
            print("ERROR: too many channel pins")
            return
        #for i,pinNum in enumerate(channelPins):
            #print(i,pinNum)
        self.pins[0] = Pin(channelPins[0], Pin.IN, Pin.PULL_UP)
        self.statemachines[0] = rp2.StateMachine(0, PIOProgs[0], freq=4_000_000, in_base=self.pins[0], jmp_pin=self.pins[0])
        self.statemachines[0].irq(lambda statemac: handler(statemac, self.results,self.resultsNorm, 0))
        self.statemachines[0].active(1)
        
        self.pins[1] = Pin(channelPins[1], Pin.IN, Pin.PULL_UP)
        self.statemachines[1] = rp2.StateMachine(1, PIOProgs[1], freq=4_000_000, in_base=self.pins[1], jmp_pin=self.pins[1])
        self.statemachines[1].irq(lambda statemac: handler(statemac, self.results,self.resultsNorm, 1))
        self.statemachines[1].active(1)

        self.pins[2] = Pin(channelPins[2], Pin.IN, Pin.PULL_UP)
        self.statemachines[2] = rp2.StateMachine(2, PIOProgs[2], freq=4_000_000, in_base=self.pins[2], jmp_pin=self.pins[2])
        self.statemachines[2].irq(lambda statemac: handler(statemac, self.results,self.resultsNorm, 2))
        self.statemachines[2].active(1)
        
        self.pins[3] = Pin(channelPins[3], Pin.IN, Pin.PULL_UP)
        self.statemachines[3] = rp2.StateMachine(3, PIOProgs[3], freq=4_000_000, in_base=self.pins[3], jmp_pin=self.pins[3])
        self.statemachines[3].irq(lambda statemac: handler(statemac, self.results,self.resultsNorm, 3))
        self.statemachines[3].active(1)

    def MappedChannel(self, chan, mn, mx):
        return mapFromNormalized(self.resultsNorm[chan], mn, mx)
        