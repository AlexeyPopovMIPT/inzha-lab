import RPi.GPIO as GPIO
import time

tr_pin = 17
cmp_pin = 4
GPIO_pins = (26, 19, 13, 6, 5, 11, 9, 10)#(21, 20, 16, 12, 7, 8, 25, 24)

def num2dac(value):
    if value > 255 or value < 0: raise ValueError
    for i in range(7, -1, -1):
        GPIO.output(GPIO_pins[i], value % 2)
        value //= 2  


GPIO.setmode(GPIO.BCM)

GPIO.setup(tr_pin, GPIO.OUT)
GPIO.setup(cmp_pin, GPIO.IN)
GPIO.setup(GPIO_pins, GPIO.OUT)

num2v = lambda num: 3.209 * num / 253

try:
    GPIO.output(tr_pin, 1)
    while True:
        for i in range(256):
            num2dac(i)
            time.sleep(0.0002)
            if GPIO.input(cmp_pin) == 0 or i == 255:
                print("Digital value: ", i, ", Analog value: ", num2v(i), " V", sep = "")
                break
except KeyboardInterrupt:
    print("keyboard interrupt")
finally:
    GPIO.cleanup()