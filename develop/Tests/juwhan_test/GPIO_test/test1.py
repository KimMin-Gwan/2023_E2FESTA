import RPi.GPIO as GPIO
import time

# GPIO 핀 번호 설정
button_pin = 18

# GPIO 모드 설정
GPIO.setmode(GPIO.BCM)

# 버튼 핀 입력으로 설정 및 풀업 저항 적용
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# 버튼 상태 변수 초기화
button_pressed_time = None

def button_pressed(channel):
    global button_pressed_time
    if GPIO.input(button_pin) == GPIO.LOW:
        button_pressed_time = time.time()

def button_released(channel):
    global button_pressed_time
    if button_pressed_time is not None:
        button_released_time = time.time()
        button_duration = button_released_time - button_pressed_time
        if button_duration >= 3:
            print("no")
        else:
            print("yes")
        button_pressed_time = None

# GPIO 이벤트 핸들러 등록
GPIO.add_event_detect(button_pin, GPIO.BOTH, callback=button_pressed)
GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=button_released, bouncetime=300)

try:
    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()