"""Camera control and capture functionality."""

import tempfile
from picamera2 import Picamera2


class Camera:
    """Wrapper for Picamera2 operations."""
    
    def __init__(self):
        """Initialize camera and start preview."""
        self.picam2 = Picamera2()
        # Configure for maximum resolution (4608x2592)
        """
        1536x864 @ 120 fps
        2304x1296 @ 56 fps
        4608x2592 @ 14 fps
        """
        config = self.picam2.create_still_configuration(main={"size": (4608, 2592)})
        self.picam2.configure(config)
        self.picam2.start()
    
    def capture_photo(self, filepath):
        """
        Capture a photo to the specified filepath.
        
        Args:
            filepath: Path where the photo will be saved
        """
        self.picam2.capture_file(filepath)
    
    def capture_video(self, filepath, duration=5):
        """
        Capture a video to the specified filepath.
        
        Args:
            filepath: Path where the video will be saved
            duration: Length of video in seconds (default: 5)
        """
        self.picam2.start_and_record_video(filepath, duration=duration)
    
    def capture_photo_to_temp(self):
        """
        Capture a photo to a temporary file.
        
        Returns:
            str: Path to the temporary file (caller must delete)
        """
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            temp_path = tmp.name
        self.picam2.capture_file(temp_path)
        return temp_path
