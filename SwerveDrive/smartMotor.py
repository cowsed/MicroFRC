from encoder import Encoder
from PID import PID
from motor import Motor

class SmartMotor:
    #Encoder, PID Values, Motor, watcher func. called when the encoder ticks. can be watched for odometry or speed information
    def __init__(self, e: Encoder, p: PID, m: Motor, watcherFunc = lambda p: p):
        self.enc = e
        self.enc.watcher = self.HandleEncoderTick
        self.pid = p
        self.motor = m
        self.watcher = watcherFunc

    def GetPosition(self):
        return self.enc.position
    def SetPosition(self, pos):
        self.pid.Set(pos)

    #Called when the enoder enters a new position. Used to update the pid controller at a high frequency and to announce to any watchers that the motor has changed
    def HandleEncoderTick(self, position):

        motorVal = self.pid.GetControl(position)
        self.motor.SetPercentOutput(motorVal)

        self.watcher(position)
