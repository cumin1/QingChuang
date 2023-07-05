
import RPi.GPIO as GPIO
import time as t
pin=16
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin,GPIO.OUT)

while True:
    GPIO.output(pin,GPIO.HIGH)
    t.sleep(1)
    GPIO.output(pin, GPIO.LOW)
    t.sleep(0)
GPIO.cleanup()





