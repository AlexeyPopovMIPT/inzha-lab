import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt
import numpy


TroikaModulePin = 17
ComparePin = 4
DAC = (26, 19, 13, 6, 5, 11, 9, 10)
LEDS = (21, 20, 16, 12, 7, 8, 25, 24)

MAX_VOLTAGE = 3.3 #V

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
        print(start)
        return start
    else:
        print(end)
        return end

def analog(digital_voltage):
    return MAX_VOLTAGE * digital_voltage / 255


try:

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TroikaModulePin, GPIO.OUT)
    GPIO.setup(ComparePin, GPIO.IN)
    GPIO.setup(DAC, GPIO.OUT)
    GPIO.setup(LEDS, GPIO.OUT)

    measurements = [] # [ (time0, volt0), (time1, volt1), ...]
    voltage = 0
    raw = []

    GPIO.output(TroikaModulePin, 0)
    time.sleep(0.1)

    START_TIME = time.time()
    GPIO.output(TroikaModulePin, 1)

    while voltage < 250:
        voltage = adc()
        raw.append(voltage)
        measurements.append((time.time() - START_TIME, analog(voltage)))
        time.sleep(0.002)

    GPIO.output(TroikaModulePin, 0)
    while voltage > 3:
        voltage = adc()
        raw.append(voltage)
        measurements.append((time.time() - START_TIME, analog(voltage)))
        time.sleep(0.002)

    numpy.savetxt('data.txt', raw, fmt='%d')

    dT = 0
    for i in range(1, len(measurements)):
        dT += measurements[i][0] - measurements[i-1][0]
    dT /= len(measurements) - 1
    dV = MAX_VOLTAGE / 255

    with open("settings.txt", "w") as settings:
        settings.write(str(dT)+"\n"+str(dV))

    plt.plot([measure[0] for measure in measurements], 
             [measure[1] for measure in measurements])

    plt.title('U(t)')
    plt.xlabel('Время, с')
    plt.ylabel('Напряжение, В')
    plt.show()


finally:

    GPIO.cleanup()




