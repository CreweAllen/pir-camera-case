#!/usr/bin/env python3
"""Motion-triggered photo capture to local filesystem."""

import time
from camera import PIRSensor, Camera, get_timestamp

# Initialize components
pir = PIRSensor(pin=17)
camera = Camera()

try:
	time.sleep(5)
	print("Ready")

	while True:
		if pir.motion_detected():
			
			print("Motion Detected!")
			
			timestamp = get_timestamp()
			image_name = f'/home/james/Programs/security-camera-output/IMG_{timestamp}.jpg'

			camera.capture_photo(image_name)

			time.sleep(2)
			print("Ready")

		time.sleep(1)

except KeyboardInterrupt:
	print("Quit")
	PIRSensor.cleanup()
