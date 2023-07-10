import RPi.GPIO as GPIO
import time

BUTTON_PIN = 16
LED_PIN = 22

GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_PIN, GPIO.OUT)

def button_callback(channel):
    if GPIO.input(BUTTON_PIN) == GPIO.LOW:
        time.sleep(0.1)  # 디바운스를 위한 지연 시간
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            start_time = time.time()
            while GPIO.input(BUTTON_PIN) == GPIO.LOW:
                pass  # 버튼이 눌려 있는 동안 대기
            end_time = time.time()
            elapsed_time = end_time - start_time
            if elapsed_time >= 3.0:
                print("A")
            else:
                print("B")

GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=200)

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()