import RPi.GPIO as GPIO
import time

# GPIO 핀 번호 설정
button_pin = 18

# GPIO 모드 설정
GPIO.setmode(GPIO.BCM)

# 버튼 핀 입력으로 설정 및 풀업 저항 적용
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def button_callback(channel):
    print("Button Pressed")

# GPIO 이벤트 핸들러 등록
GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=button_callback, bouncetime=300)

try:
    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()