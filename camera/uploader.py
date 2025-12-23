"""Cloud upload functionality for images."""

import requests


class CloudUploader:
    """Handles uploading images to cloud endpoints."""
    
    def __init__(self, base_url, headers=None, website_id="cotmarshtannery", camera_name="Security1"):
        """
        Initialize cloud uploader.
        
        Args:
            base_url: Base URL of the Azure Function or API endpoint
            headers: Optional HTTP headers dict (defaults to image/jpeg Content-Type)
            website_id: Website identifier for the upload
            camera_name: Camera name/identifier
        """
        self.base_url = base_url
        self.headers = headers or {"Content-Type": "image/jpeg"}
        self.website_id = website_id
        self.camera_name = camera_name
    
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
        params = {
            "websiteId": self.website_id,
            "cameraName": self.camera_name
        }
        
        # Create a copy of headers to avoid modifying instance headers
        request_headers = self.headers.copy()
        
        # Add function key to params if provided (Azure Functions use 'code' parameter)
        if request_headers.get("x-functions-key"):
            params["code"] = request_headers.pop("x-functions-key")
        
        try:
            # Read file content into memory to ensure Content-Type header is sent properly
            with open(image_path, "rb") as f:
                image_data = f.read()
            
            resp = requests.put(url, data=image_data, headers=request_headers, params=params, timeout=30)
            
            if resp.ok:
                print(f"Uploaded photo {timestamp} -> {url} (status {resp.status_code})")
                return True
            else:
                print(f"Upload failed to: {resp.url}")
                print(f"Status: {resp.status_code}, Body: {resp.text}")
                return False
        except requests.RequestException as e:
            print(f"HTTP upload error to {url}: {e}")
            return False
