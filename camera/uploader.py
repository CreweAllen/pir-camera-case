"""Cloud upload functionality for images."""

import requests


class CloudUploader:
    """Handles uploading images to cloud endpoints."""
    
    def __init__(self, base_url, headers=None):
        """
        Initialize cloud uploader.
        
        Args:
            base_url: Base URL of the Azure Function or API endpoint
            headers: Optional HTTP headers dict (defaults to image/jpeg Content-Type)
        """
        self.base_url = base_url
        self.headers = headers or {"Content-Type": "image/jpeg"}
    
    def upload_image(self, image_path, timestamp):
        """
        Upload an image file to the cloud endpoint.
        
        Args:
            image_path: Path to the image file to upload
            timestamp: Timestamp string for logging
            
        Returns:
            bool: True if upload succeeded, False otherwise
        """
        if not self.base_url:
            print("BASE_URL not configured; skipping upload")
            return False
        
        url = self.base_url.rstrip("/") + "/api/camera/photo"
        try:
            with open(image_path, "rb") as f:
                resp = requests.put(url, data=f, headers=self.headers, timeout=30)
            
            if resp.ok:
                print(f"Uploaded photo {timestamp} -> {url} (status {resp.status_code})")
                return True
            else:
                print(f"Upload failed: status {resp.status_code}, body: {resp.text}")
                return False
        except requests.RequestException as e:
            print(f"HTTP upload error: {e}")
            return False
