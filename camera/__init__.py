"""
Security Camera Package
Provides components for PIR sensor, camera control, and cloud upload.
"""

from .sensor import PIRSensor
from .capture import Camera
from .uploader import CloudUploader
from .config import CameraConfig
from .utils import get_timestamp, safe_delete_file

__all__ = [
    'PIRSensor',
    'Camera', 
    'CloudUploader',
    'CameraConfig',
    'get_timestamp',
    'safe_delete_file'
]

__version__ = '1.0.0'
