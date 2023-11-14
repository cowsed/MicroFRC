#PID Controller
#Assumes uniform spacing of calls to GetControl - derivative and integral have no concept of time
class PID:
    def __init__(self, proportionalTerm: float, integralTerm: float, derivativeTerm: float, historyLength: int = 10):
        self.setpoint = 0

        self.kP: float = proportionalTerm
        self.kI: float = integralTerm
        self.kD: float = derivativeTerm

        self.integral = 0
        self.lastErr = 0


    #Takes the measurede process variable and returns the output (input encoder position, output motor power)
    def GetControl(self, PV: float)->float:
        e: float = self.setpoint-PV #Calculated error
        self.integral += e

        i = self.integral
        d = (self.e - self.lastErr)

        self.lastErr = e
        return (self.kP * e) + (self.kI * i) + (self.kD * d)


    #Sets the setpoint of the controller
    def Set(self, sp):
        self.setpoint = sp
        #self.integral = 0


def main():
    con = PID(.5,.01,0)
    con.Set(120)

    print(con.GetControl(0))
    print(con.GetControl(20))
    print(con.GetControl(60))
    print(con.GetControl(120))
    print(con.GetControl(140))
    #print(con.GetControl(60))
    pass

if __name__=='__main__':
    main()
