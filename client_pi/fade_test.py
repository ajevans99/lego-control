import RPi.GPIO as GPIO
from time import sleep
import random

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) ## Indicates which pin numbering configuration to use

ledMouth = 8

GPIO.setup(ledMouth, GPIO.OUT)
GPIO.output(ledMouth, GPIO.HIGH)

led = GPIO.PWM(ledMouth, 100)

led.start(0)         
pause_time = 0.02

try:
    while True:
        for x in range(0,1):
            for i in range(0,101):      # 101 because it stops when it finishes 100
                led.ChangeDutyCycle(i)
                sleep(pause_time)
                print(i)
            for i in range(100,-1,-1):      # from 100 to zero in steps of -1
                led.ChangeDutyCycle(i)
                sleep(pause_time)
                print(i)

except KeyboardInterrupt:
    GPIO.cleanup()
