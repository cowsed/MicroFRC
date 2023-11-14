from machine import Pin,PWM

def clamp(l,h,v):
    if v<l:
        return l
    if v>h:
        return h
    return v

# A motor controller for the TB6612FNG motor controller
# https://www.sparkfun.com/datasheets/Robotics/TB6612FNG.pdf?_ga=2.188344170.378337409.1645108327-1775056063.1645108327
class Motor: 

    Frequency = 1000
    def __init__(self, Pin1Num: int, Pin2Num: int,PWMPinNum: int, reverse: bool = False, deadzone: float = .1):
        self.Pin1 = Pin(Pin1Num, Pin.OUT)
        self.Pin2 = Pin(Pin2Num, Pin.OUT)
        
        self.PWM = PWM(Pin(PWMPinNum))
        self.PWM.freq(self.Frequency)
        self.reverse = reverse
        self.deadzone=deadzone
        
    # Set the motor power with range from -1 (full reverse) to 1 (full forward)
    def SetPercentOutput(self,speed: float)->None:
        # Constrain speed to acceptable values
        speed = clamp(-1,1,speed)
        dutyCycle = speed
        # Get duty cycle to positive
        if(speed < 0):
            dutyCycle = dutyCycle * -1
        
        # Don't start the motors unless the speed exceeds the deadzone
        # This prevents the motors from whining if they dont have enough torque at a lower speed
        if dutyCycle<self.deadzone:
            dutyCycle = 0
        
        # If the motor was set up as reversed, flip around the speed
        if(self.reverse):
            speed = speed * -1

        # Set Direction Pins
        if(speed > 0):
            self.Pin1.on()
            self.Pin2.off()
        else:
            self.Pin1.off()
            self.Pin2.on()
        
        #Set Magnitude of speed
        self.PWM.duty_u16(int(dutyCycle*65535))
    
    # Stop the motor
    def brake(self) -> None:
        self.PWM.duty_u16(0)
        self.Pin1.on()
        self.Pin2.on()



