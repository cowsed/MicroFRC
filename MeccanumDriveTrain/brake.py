from Motor.Controller import Motor

BRMotor = Motor(16,17,18, rev=True)
FRMotor = Motor(19,20,21)
FLMotor = Motor(26,27,22, rev=True)
BLMotor = Motor(13,14,15)


BRMotor.SetPercentOutput(0)
FRMotor.SetPercentOutput(0)
BLMotor.SetPercentOutput(0)
FLMotor.SetPercentOutput(0)
