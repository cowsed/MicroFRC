#https://cdn.sparkfun.com/datasheets/Robotics/How%20to%20use%20a%20quadrature%20encoder.pdf



#doFunc is a function called when an encoder is ticked. default to nothing. when used as part of a pid controller can be used to set new values for the motor faster than a main control loop
class Encoder:    
    def __init__(self, pinNumA, pinNumB, watchFunc = lambda p: p):
        self.APin = Pin(pinNumA, Pin.IN)
        self.BPin = Pin(pinNumB, Pin.IN)
        self.APin.irq(self.PinIntA)
        self.BPin.irq(self.PinIntB)
        
        self.lastState = 0b00
        self.currState = 0b00
        
        self.aVal = self.APin.value()
        self.bVal = self.BPin.value()
        
        self.pos = 0

        invalid = .5
        self.Control = [0, -1, 1, invalid,1,0,invalid,-1,-1,invalid, 0, 1, invalid, 1, -1, 0]
        
        self.watcher = watchFunc
        
    def calcDir(self):
        self.currState = self.aVal*2 + self.bVal
        delta = self.Control[self.lastState*4 + self.currState]
        self.pos+=delta
        self.lastState = self.currState
        self.watcher(self.pos)
        
    def PinIntA(self,p):
        self.aVal = p.value()
        self.calcDir()
    def PinIntB(self,p):
        self.bVal = p.value()
        self.calcDir()