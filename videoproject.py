import RPi.GPIO as GPIO
from picamera2 import Picamera2
import time
from datetime import datetime

GPIO.setmode(GPIO.BCM)
PIR_PIN = 17
GPIO.setup(PIR_PIN, GPIO.IN)

picam2 = Picamera2()
# video_config = picam2.create_video_configuration()
# picam2.configure(video_config)

try:
	time.sleep(5)
	print("Ready")

	while True:
		if GPIO.input(PIR_PIN):
			print("Motion Detected!")
			timestamp = time.strftime("%Y%m%d-%H%M%S")
			video_name = f'/home/james/Videos/security-camera/VID_{timestamp}.mp4'
			#picam2.start_recording(encoder="libx264", output=video_name)
			#time.sleep(10)
			#picam2.stop_recording()
			#time.sleep(2)
			picam2.start_and_record_video(video_name, duration=5)
			print("Ready")
		time.sleep(1)

except KeyboardInterrupt:
	print("Quit")
	GPIO.cleanup()