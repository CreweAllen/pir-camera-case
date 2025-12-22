"""Utility functions for security camera operations."""

import os
import time


def get_timestamp():
    """
    Generate a timestamp string in YYYYMMDD-HHMMSS format.
    
    Returns:
        str: Formatted timestamp string
    """
    return time.strftime("%Y%m%d-%H%M%S")


def safe_delete_file(filepath):
    """
    Safely delete a file, ignoring errors if it doesn't exist.
    
    Args:
        filepath: Path to the file to delete
    """
    try:
        os.remove(filepath)
    except OSError:
        pass
