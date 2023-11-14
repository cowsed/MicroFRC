from PIDControl.PIDController import PID
from encoder import Encoder
from motor import Motor
from smartMotor import SmartMotor
from math import atan2, degrees


class TwoWheelSwerve:

    def __init__(self, leftSteerMot: SmartMotor, rightSteerMot: SmartMotor):
        self.leftSteerMotor = leftSteerMot
        self.rightSteerMotor = rightSteerMot
    
    def HandleInput(self, x: float, y: float, rot: float):
        #Point wheels at x,y
        #   Get current position of each
        #   Find closest equivalent angle (360=0)
        #   Set to that point
        ang = degrees(atan2(y,x))
        self.leftSteerMotor.SetPosition(ang)
        pass


def main():
    tre = Encoder(8,9)
    trmotor = Motor(1,2,3,rev=False, deadzone=.1)
    trPID = PID(.5,0,0)
    TR = SmartMotor(tre, trPID, trmotor)
    
    TWSwerve = TwoWheelSwerve(TR, None)
    while True:
        desiredX = int(input("Enter Position X:\n"))
        desiredY = int(input("Enter Position Y:\n"))
        TWSwerve.HandleInput(desiredX, desiredY)
        