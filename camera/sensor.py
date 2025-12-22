"""PIR motion sensor control."""

import RPi.GPIO as GPIO


class PIRSensor:
    """Wrapper for PIR sensor GPIO operations."""
    
    def __init__(self, pin=17):
        """
        Initialize PIR sensor.
        
        Args:
            pin: GPIO pin number where PIR sensor is connected (BCM numbering)
        """
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)
    
    def motion_detected(self):
        """
        Check if motion is currently detected.
        
        Returns:
            bool: True if motion detected, False otherwise
        """
        return GPIO.input(self.pin)
    
    @staticmethod
    def cleanup():
        """Clean up GPIO resources."""
        GPIO.cleanup()
