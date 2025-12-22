#!/usr/bin/env python3
"""Motion-triggered photo capture with cloud upload."""

import time
from camera import (
    CameraConfig, PIRSensor, Camera, CloudUploader,
    get_timestamp, safe_delete_file
)

# Initialize configuration
config = CameraConfig()

if not config.base_url:
    print("Error: BASE_URL environment variable is not set. Set it to https://<app>.azurewebsites.net")

# Initialize components
pir = PIRSensor(config.pir_pin)
camera = Camera()
uploader = CloudUploader(config.base_url, config.get_upload_headers())

try:
    time.sleep(5)
    print("Ready")

    while True:
        if pir.motion_detected():
            print("Motion Detected!")
            timestamp = get_timestamp()

            # Capture to a temporary file, then upload to cloud
            temp_path = camera.capture_photo_to_temp()

            try:
                uploader.upload_image(temp_path, timestamp)
            finally:
                safe_delete_file(temp_path)

            time.sleep(2)
            print("Ready")

        time.sleep(1)

except KeyboardInterrupt:
    print("Quit")
    PIRSensor.cleanup()
