from machine import Pin
import time

pin = Pin(25, Pin.OUT)
print("toggle")
for i in range(10):
    pin.toggle()
    time.sleep_ms(200)
