import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(23, GPIO.IN)
state=0

try:
    while True:
        inputIO=GPIO.input(23)
        if inputIO ==False:
            if state==0:
                state=1
                GPIO.output(21, GPIO.HIGH)
                time.sleep(1)
            elif state==1:
                GPIO.output(21, GPIO.LOW)
                state=0
                time.sleep(1)
except KeyboardInterrupt:
    GPIO.output(21, GPIO.LOW)

finally:
    GPIO.cleanup()