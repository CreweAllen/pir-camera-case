import RPi.GPIO as GPIO
from picamera2 import Picamera2
import time
from datetime import datetime 

GPIO.setmode(GPIO.BCM)
PIR_PIN = 17
GPIO.setup(PIR_PIN, GPIO.IN)

picam2 = Picamera2()
picam2.start()

try:
	time.sleep(5)
	print("Ready")

	while True:
		if GPIO.input(PIR_PIN):
			
			print("Motion Detected!")
			
			timestamp = time.strftime("%Y%m%d-%H%M%S")
			image_name = f'/home/james/Videos/security-camera/IMG_{timestamp}.jpg'

			picam2.capture_file(image_name)

			time.sleep(2)
			print("Ready")

		time.sleep(1)

except KeyboardInterrupt:
	print("Quit")
	GPIO.cleanup()