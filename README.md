# Security Camera with Cloud Upload

This guide explains how to set up and run the PIR motion-sensing camera with automatic photo upload to Azure Functions.

## Overview

The cloud-enabled scripts extend the basic motion-sensing camera functionality by automatically uploading captured photos to an Azure Function endpoint via HTTP PUT requests. This enables cloud storage, processing, and remote access to captured images.

## Project Structure

```
pir-camera-case/
├── camera/                    # Core library modules
│   ├── config.py             # Configuration management
│   ├── sensor.py             # PIR sensor control
│   ├── capture.py            # Camera operations
│   ├── uploader.py           # Cloud upload functionality
│   └── utils.py              # Utility functions
├── scripts/                   # Executable scripts
│   ├── photo_motion.py       # Local photo capture (motion-triggered)
│   ├── video_motion.py       # Local video capture (motion-triggered)
│   ├── cloud_motion.py       # Cloud photo upload (motion-triggered)
│   └── cloud_scheduled.py    # Cloud photo upload (scheduled)
├── systemd/                   # Service configuration
│   ├── photo-cloud.service   # Systemd service
│   └── photo-cloud.timer     # Timer for scheduled runs
└── requirements.txt           # Python dependencies
```

## Features

- **Motion Detection**: Uses PIR sensor to detect movement
- **Automatic Photo Capture**: Takes photos when motion is detected using Picamera2
- **Cloud Upload**: Automatically uploads images to Azure Functions
- **Temporary File Handling**: Uses temporary files for efficient memory management
- **Configurable**: Environment variables for easy deployment configuration
- **Function Key Support**: Optional Azure Function authentication

## Prerequisites

- Raspberry Pi with Camera Module and PIR sensor (assembled in PIR Camera Case)
- Python 3
- Required Python packages (see [Installation](#installation))
- Azure Function App configured to receive image uploads (or compatible HTTP endpoint)

## Installation

1. **Clone/Download the Repository** (if not already done):
```bash
git clone https://github.com/ThePiHut/pir-camera-case
cd pir-camera-case
```

2. **Install Required Python Packages**:
```bash
pip install -r requirements.txt
```

## Configuration

The script uses environment variables for configuration. Set these before running:

### Required Environment Variables

- **`BASE_URL`**: The base URL of your Azure Function App
  ```bash
  export BASE_URL="https://your-app.azurewebsites.net"
  ```

### Optional Environment Variables

- **`PIR_PIN`**: GPIO pin number for PIR sensor (default: 17)
  ```bash
  export PIR_PIN="17"
  ```

- **`AZURE_FUNCTION_KEY`**: Azure Function authentication key (if required)
  ```bash
  export AZURE_FUNCTION_KEY="your-function-key-here"
  ```

## Azure Function Endpoint

The script uploads images to: `{BASE_URL}/api/camera/photo`

### Expected Azure Function Behavior

Your Azure Function should:
- Accept HTTP PUT requests
- Expect `Content-Type: image/jpeg` header
- Optionally validate `x-functions-key` header for authentication
- Return HTTP 2xx status on successful upload
- Handle binary image data in request body

### Example Azure Function (Node.js)

```javascript
module.exports = async function (context, req) {
    if (req.method === 'PUT') {
        const imageBuffer = req.body;
        const timestamp = new Date().toISOString();
        
        // Store to Azure Blob Storage, process, etc.
        // ... your storage logic here ...
        
        context.res = {
            status: 200,
            body: { message: "Image uploaded successfully", timestamp }
        };
    } else {
        context.res = {
            status: 405,
            body: "Method not allowed"
        };
    }
};
```

## Running the Scripts

### Manual Execution

**Motion-Detected Mode** (continuous monitoring):
```bash
export BASE_URL="https://your-app.azurewebsites.net"
export AZURE_FUNCTION_KEY="your-key-here"  # Optional
cd /home/james/repos/Personal/pir-camera-case
sudo python3 scripts/cloud_motion.py
```

**Scheduled Mode** (single capture):
```bash
export BASE_URL="https://your-app.azurewebsites.net"
export AZURE_FUNCTION_KEY="your-key-here"  # Optional
cd /home/james/repos/Personal/pir-camera-case
sudo python3 scripts/cloud_scheduled.py
```

### Running as a Scheduled Systemd Service (Recommended)

For scheduled photo captures at specific times (09:00, 12:00, and 18:00 daily), use the timer-based systemd service.

1. **Copy both service and timer files to systemd**:
   ```bash
   sudo cp /home/james/repos/Personal/pir-camera-case/systemd/photo-cloud.service /etc/systemd/system/
   sudo cp /home/james/repos/Personal/pir-camera-case/systemd/photo-cloud.timer /etc/systemd/system/
   ```

2. **Reload systemd**:
   ```bash
   sudo systemctl daemon-reload
   ```

3. **Enable and start the timer**:
   ```bash
   sudo systemctl enable photo-cloud.timer
   sudo systemctl start photo-cloud.timer
   ```

4. **Check timer status**:
   ```bash
   sudo systemctl status photo-cloud.timer
   sudo systemctl list-timers photo-cloud.timer
   ```

5. **View logs**:
   ```bash
   sudo journalctl -u photo-cloud.service -f
   ```

### Running as a Systemd Service (Continuous Motion Detection)

For continuous operation with motion detection, modify the service file:

1. **Edit the service file**:
   ```bash
   sudo nano /etc/systemd/system/photo-cloud.service
   ```

2. **Change to continuous mode**:
   ```ini
   [Service]
   Type=simple
   ExecStart=/usr/bin/python3 /home/james/repos/Personal/pir-camera-case/scripts/cloud_motion.py
   Restart=on-failure
   ```

3. **Reload and start**:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable photo-cloud.service
   sudo systemctl start photo-cloud.service
   ```

## How It Works

1. **Initialization**: 
   - Configures GPIO for PIR sensor (BCM pin 17 by default)
   - Initializes Picamera2
   - Reads configuration from environment variables

2. **Main Loop**:
   - Continuously monitors PIR sensor for motion
   - When motion detected:
     - Generates timestamp (format: `YYYYMMDD-HHMMSS`)
     - Captures image to temporary file
     - Uploads image to Azure Function via HTTP PUT
     - Deletes temporary file
     - Waits 2 seconds before resuming monitoring

3. **Upload Process**:
   - Creates HTTP PUT request to `{BASE_URL}/api/camera/photo`
   - Includes image data as binary in request body
   - Sets `Content-Type: image/jpeg` header
   - Optionally includes `x-functions-key` for authentication
   - Times out after 30 seconds

## Troubleshooting

### Upload Failures

**Issue**: Photos not uploading to Azure Function

**Solutions**:
- Verify `BASE_URL` is correctly set
- Check network connectivity: `ping your-app.azurewebsites.net`
- Verify Azure Function is running and accessible
- Check function key authentication if enabled
- Review console output for HTTP error messages

### Environment Variables Not Set

**Issue**: Script reports "BASE_URL not configured"

**Solutions**:
- Export `BASE_URL` before running script
- Add environment variables to systemd service file
- Verify variables with: `echo $BASE_URL`

### Permission Errors

**Issue**: GPIO or camera access denied

**Solutions**:
- Run script with `sudo`
- Add user to `gpio` and `video` groups:
  ```bash
  sudo usermod -a -G gpio,video $USER
  ```
- Reboot after adding to groups

### Excessive False Triggers

**Issue**: Too many photos being captured

**Solutions**:
- Adjust PIR sensitivity dial (see main [README.md](README.md))
- Increase wait time after capture (modify `time.sleep(2)` in code)
- Check for heat sources or WiFi interference near sensor

## Security Considerations

- **Function Keys**: Store Azure Function keys securely, don't commit to version control
- **Network Security**: Use HTTPS endpoints (Azure Functions use HTTPS by default)
- **Access Control**: Implement proper authentication on your Azure Function
- **Data Privacy**: Ensure compliance with privacy regulations when capturing/storing images

## Related Files

### Scripts
- [scripts/cloud_motion.py](scripts/cloud_motion.py) - Motion-triggered cloud upload
- [scripts/cloud_scheduled.py](scripts/cloud_scheduled.py) - Scheduled cloud upload  
- [scripts/photo_motion.py](scripts/photo_motion.py) - Local photo capture (motion)
- [scripts/video_motion.py](scripts/video_motion.py) - Local video capture (motion)

### Library Modules
- [camera/config.py](camera/config.py) - Configuration management
- [camera/sensor.py](camera/sensor.py) - PIR sensor control
- [camera/capture.py](camera/capture.py) - Camera operations
- [camera/uploader.py](camera/uploader.py) - Cloud upload functionality
- [camera/utils.cripts/cloud_scheduled.py`
- **Trigger**: Systemd timer at 09:00, 12:00, 18:00
- **Use Case**: Regular interval monitoring, lower power consumption
- **Setup**: Uses `photo-cloud.timer` and `photo-cloud.service`

### Motion Detection Mode (Continuous)
- **Script**: `scripts/cloud_motion.py`
- **Trigger**: PIR motion sensor
- **Use Case**: Security monitoring, event-driven captures
- **Setup**: Uses `photo-cloud.service`
## Operation Modes

### Scheduled Mode (Timer-Based)
- **Script**: `security-camera-photo-cloud-scheduled.py`
- **Trigger**: Systemd timer at 09:00, 12:00, 18:00
- **Use Case**: Regular interval monitoring, lower power consumption
- **Setup**: Uses `.timer` and `.service` files

### Motion Detection Mode (Continuous)
- **Script**: `security-camera-photo-cloud.py`
- **Trigger**: PIR motion sensor
- **Use Case**: Security monitoring, event-driven captures
- **Setup**: Uses `.service` file with `Type=simple` and `Restart=on-failure`

## Differences from Local-Only Scripts

| Feature | Cloud Upload | Local Only |
|---------|-------------|------------|
| Storage | Azure Function/Cloud | Local filesystem |
| Configuration | Environment variables | Hardcoded paths |
| Dependencies | `requests` library | None (only GPIO/picamera) |
| File Management | Temporary files (auto-deleted) | Permanent files with timestamp |
| Network Required | Yes | No |
| Remote Access | Yes (via cloud) | No |

## Example Output

```
Ready
Motion Detected!
Uploaded photo 20251222-143052 -> https://your-app.azurewebsites.net/api/camera/photo (status 200)
Ready
Motion Detected!
Uploaded photo 20251222-143108 -> https://your-app.azurewebsites.net/api/camera/photo (status 200)
Ready
^CQuit
```

## License

This project follows the same license as the main PIR Camera Case repository.

## Support

For issues specific to:
- **PIR Camera Case hardware**: See main [README.md](README.md)
- **Azure Functions**: Consult [Azure Functions documentation](https://docs.microsoft.com/azure/azure-functions/)
- **This script**: Open an issue in the repository
