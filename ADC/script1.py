import RPi.GPIO as GPIO

GPIO_pins = (26, 19, 13, 6, 5, 11, 9, 10)
tr_pin = 17

def num2dac(value):
    if value > 255 or value < 0: raise ValueError
    for i in range(7, -1, -1):
        GPIO.output(GPIO_pins[i], value % 2)
        value //= 2  


GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_pins, GPIO.OUT)
GPIO.setup(tr_pin, GPIO.OUT)

num2v = lambda num: 3.257 * nmb / 255

try:
    GPIO.output(tr_pin, 1)
    while True:
        nmb = int(input("Enter value (-1 to exit) > "))
        if (nmb == -1): break
        num2dac(nmb)
        print(nmb, " = ", num2v(nmb), " V", sep="")

except ValueError:
    print("Ошибка: ожидалось целое число от 0 до 255")

finally:
    GPIO.cleanup()