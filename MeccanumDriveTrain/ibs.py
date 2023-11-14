# uart ibus test with micropython in pico
# works with flysky fs-i6x transmitter
# fs-rx2a pro receiver
# ibus protocol 32 bytes sent UART 115200 baud 8n1
# channel value range are 1000 - 2000 (1500 middle, good for servo)
#
# replace _lt_ with less than sign, youtube don't like angle brackets
#
#   0x20 0x40 - header
#   0xDC 0x05 - 1500 value (little endian 0x05 0xDC) channel 1
#   0xXX 0xXX - channel 2
#   0xXX 0xXX - channel 3
#   0xXX 0xXX - channel 4
#   0xXX 0xXX - channel 5
#   0xXX 0xXX - channel 6
#   0xXX 0xXX - channel 7
#   0xXX 0xXX - channel 8
#   0xXX 0xXX - channel 9
#   0xXX 0xXX - channel 10
#   0xXX 0xXX - channel 11
#   0xXX 0xXX - channel 12
#   0xXX 0xXX - channel 13
#   0xXX 0xXX - channel 14
#   0xXX 0xXX - checksum 0xFFFF minus sum of all above bytes (not including this checksum)
#
#   checksum above are also little endian

from machine import UART, Pin,PWM, Timer
import utime

    


def normal(v, mn,mx):
    return ((v-mn)/(mx-mn))
def mapFromNormalized(v, mn,mx):
    return v*(mx-mn)+mn

class IBusReceiver:
    results=[]
    header = b' @'
    def __init__(self, NumChannels):
        self.results = [1500]*NumChannels
        self.uart = UART(1, 115200, tx = Pin(4), rx = Pin(5)) # uart1 tx-pin 4, rx-pin 5
        self.numChannels = NumChannels
    def MappedChannel(self, chan, mn, mx):
        return mapFromNormalized(self.results[chan], mn, mx)
    
    def ReadReceiver(self):
        anyu = self.uart.any()
        if anyu>=32:
            self.__handleUART()
            
    def __handleUART(self):
        c=self.uart.read(32)
        if c==None:        
            return
        if len(c)!=32:
            return
        if (c[0:2]!=self.header):
            return
        index = 0
        for i in range(2,2+2*self.numChannels,2):
            lsb = c[i]
            msb = c[i+1]
            self.results[index] = normal(int(msb)*255+int(lsb),1000,2000)
            index+=1

frame =0
l = PWM(Pin(25))
def SetFraction(frac, dev):
    dev.duty_u16(int(frac*65535))

rec = IBusReceiver(10)
while True:
    rec.ReadReceiver()
    utime.sleep(.01)

    frame+=1
    if frame%10==0:
        print(rec.results)
    
    
    amt = rec.MappedChannel(0,0,1)
    SetFraction(amt, l)
