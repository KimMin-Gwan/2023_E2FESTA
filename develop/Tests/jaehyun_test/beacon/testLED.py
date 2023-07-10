import RPi.GPIO as GPIO
import time
scanButton = 8
YNButton = 10
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(scanButton, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(YNButton, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

def main():
	flag = 0
	while 1:

		if GPIO.input(scanButton) == GPIO.HIGH:
			print("1 Button Pushed")
		if flag == 1 and GPIO.input(YNButton) == GPIO.HIGH:
			continue
		elif flag == 1 and GPIO.input(YNButton) == GPIO.LOW:
			eTime =time.time()
			elapsedTime = eTime - sTime
			if elapsedTime<= 2:
				print("Yes Button Pushed")
			else:
				print("No Button Pushed")
			flag = 0
		elif flag == 0 and GPIO.input(YNButton) == GPIO.HIGH:
			flag = 1
			sTime = time.time()
		time.sleep(0.1)

if __name__ == "__main__":
	main()
