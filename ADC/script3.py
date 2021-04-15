import RPi.GPIO as GPIO
import time

tr_pin = 17
cmp_pin = 4
GPIO_pins = (26, 19, 13, 6, 5, 11, 9, 10)

def num2dac(value):
    if value > 255 or value < 0: raise ValueError
    for i in range(7, -1, -1):
        GPIO.output(GPIO_pins[i], value % 2)
        value //= 2  


GPIO.setmode(GPIO.BCM)

GPIO.setup(tr_pin, GPIO.OUT)
GPIO.setup(cmp_pin, GPIO.IN)
GPIO.setup(GPIO_pins, GPIO.OUT)

num2v = lambda num: 3.209 * num / 251

try:    
    GPIO.output(tr_pin, 1)  
    while True:
        start = 0; end = 255
        while start <= end:
            mid = (start + end) // 2
            num2dac(mid)
            time.sleep(0.005)
            if GPIO.input(cmp_pin) == 0:
                end = mid - 1
            else:
                start = mid + 1
    
        if end < 0:
            res = start
        else:
            res = end

        print("Digital value: ", res, ", Analog value: ", num2v(res), " V", sep = "")

except KeyboardInterrupt:
    print("keyboard interrupt")
finally:
    GPIO.cleanup()



















































# для тестинга двоичного поиска
def bsearch(arr, value):
    nm = len(arr)-1
    start = 0; end = nm
    while start <= end:
        mid = (start + end) // 2
        if arr[mid] > value:
            end = mid - 1
        else:
            start = mid + 1

    if end < 0:
        res = start
    else:
        res = end

    return res
