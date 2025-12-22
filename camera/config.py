"""Configuration management for security camera system."""

import os


class CameraConfig:
    """Configuration for camera and GPIO setup."""
    
    def __init__(self, pir_pin=None, base_url=None, function_key=None):
        """
        Initialize camera configuration.
        
        Args:
            pir_pin: GPIO pin number for PIR sensor (defaults to PIR_PIN env var or 17)
            base_url: Azure Function base URL (defaults to BASE_URL env var)
            function_key: Azure Function authentication key (defaults to AZURE_FUNCTION_KEY env var)
        """
        self.pir_pin = int(pir_pin or os.environ.get("PIR_PIN", "17"))
        self.base_url = base_url or os.environ.get("BASE_URL")
        self.function_key = function_key or os.environ.get("AZURE_FUNCTION_KEY")
    
    def get_upload_headers(self):
        """
        Get HTTP headers for cloud upload.
        
        Returns:
            dict: Headers with Content-Type and optional function key
        """
        headers = {"Content-Type": "image/jpeg"}
        if self.function_key:
            headers["x-functions-key"] = self.function_key
        return headers
