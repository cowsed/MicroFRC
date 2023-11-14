from math import sqrt, sin,cos

def CalcWheelAmts(desiredDirPower,desiredDirAngle, desiredDirRot, TranslationSplit):
    desiredX = cos(desiredDirAngle)
    desiredY = sin(desiredDirAngle)
    
    #global FLAmt,FRAmt, BLAmt, BRAmt
    FLAmt = 0
    FRAmt = 0
    BLAmt = 0
    BRAmt = 0
    #Y component
    FLAmt+=desiredY
    FRAmt+=desiredY
    BLAmt+=desiredY
    BRAmt+=desiredY

    #X Component
    FLAmt+=desiredX
    FRAmt-=desiredX
    BRAmt+=desiredX
    BLAmt-=desiredX
    
    mxSpeed = max(max(abs(FLAmt), abs(FRAmt)), max(abs(BRAmt), abs(BLAmt)))
    if mxSpeed == 0:
        mxSpeed = 1

    FLAmt/=mxSpeed
    BLAmt/=mxSpeed
    FRAmt/=mxSpeed
    BRAmt/=mxSpeed
    
    FLAmt*=desiredDirPower*TranslationSplit
    BLAmt*=desiredDirPower*TranslationSplit
    FRAmt*=desiredDirPower*TranslationSplit
    BRAmt*=desiredDirPower*TranslationSplit

    RotSplit = 1-TranslationSplit

    FLAmt-=desiredDirRot*RotSplit
    BLAmt-=desiredDirRot*RotSplit
    FRAmt+=desiredDirRot*RotSplit
    BRAmt+=desiredDirRot*RotSplit
    
    return FLAmt, FRAmt, BLAmt, BRAmt
    