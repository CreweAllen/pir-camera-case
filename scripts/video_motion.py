#!/usr/bin/env python3
"""Motion-triggered video capture to local filesystem."""

import time
from camera import PIRSensor, Camera, get_timestamp

# Initialize components
pir = PIRSensor(pin=17)
camera = Camera()
# video_config = camera.picam2.create_video_configuration()
# camera.picam2.configure(video_config)

try:
	time.sleep(5)
	print("Ready")

	while True:
		if pir.motion_detected():
			print("Motion Detected!")
			timestamp = get_timestamp()
			video_name = f'/home/james/Programs/security-camera-output/VID_{timestamp}.mp4'
			#camera.picam2.start_recording(encoder="libx264", output=video_name)
			#time.sleep(10)
			#camera.picam2.stop_recording()
			#time.sleep(2)
			camera.capture_video(video_name, duration=5)
			print("Ready")
		time.sleep(1)

except KeyboardInterrupt:
	print("Quit")
	PIRSensor.cleanup()
