import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt
import numpy


TroikaModulePin = 17
ComparePin = 4
DAC = (26, 19, 13, 6, 5, 11, 9, 10)
LEDS = (21, 20, 16, 12, 7, 8, 25, 24)

def num2pins(pins, num):
    for i in range(7, -1, -1):
        GPIO.output(pins[i], num % 2)
        num //= 2

def adc():
    start = 0; end = 255
    while start <= end:
        mid = (start + end) // 2
        num2pins(DAC, mid)
        time.sleep(0.0003)
        if GPIO.input(ComparePin) == 0:
            end = mid - 1
        else:
            start = mid + 1
    
    if end < 0:
        return start
    else:
        return end


try:

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TroikaModulePin, GPIO.OUT)
    GPIO.setup(ComparePin, GPIO.IN)
    GPIO.setup(DAC, GPIO.OUT)
    GPIO.setup(LEDS, GPIO.OUT)

    measure = []
    voltage = 0

    GPIO.output(TroikaModulePin, 1)
    while voltage < 250:
        voltage = adc()
        measure.append(voltage)
        # time.sleep(0.0001)

    GPIO.output(TroikaModulePin, 0)
    while voltage > 3:
        voltage = adc()
        measure.append(voltage)
        time.sleep(0.002)

    numpy.savetxt('data.txt', measure, fmt='%d')


finally:

    GPIO.cleanup()

