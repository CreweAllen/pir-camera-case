#!/usr/bin/env python3
"""Scheduled photo capture with cloud upload (no PIR sensor)."""

import time
from datetime import datetime
from camera import (
    CameraConfig, Camera, CloudUploader,
    get_timestamp, safe_delete_file
)

# Initialize configuration
config = CameraConfig()

if not config.base_url:
    print("Error: BASE_URL environment variable is not set. Set it to https://<app>.azurewebsites.net")
    exit(1)

# Initialize components
camera = Camera()
uploader = CloudUploader(config.base_url, config.get_upload_headers())


def capture_and_upload():
    """Capture a photo and upload it to the cloud."""
    timestamp = get_timestamp()
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Scheduled capture starting...")

    # Capture to a temporary file, then upload to cloud
    temp_path = camera.capture_photo_to_temp()

    try:
        print(f"Photo captured: {timestamp}")
        
        success = uploader.upload_image(temp_path, timestamp)
        if success:
            print(f"✓ Successfully uploaded photo at {timestamp}")
        else:            
            print(f"✗ Failed to upload photo at {timestamp}")
        
        return success

    finally:
        safe_delete_file(temp_path)


if __name__ == "__main__":
    try:
        # Allow camera to warm up
        time.sleep(2)
        
        # Capture and upload immediately when script runs
        capture_and_upload()
        
    except KeyboardInterrupt:
        print("Quit")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
