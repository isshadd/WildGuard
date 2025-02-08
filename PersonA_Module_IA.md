# Person A - AI Detection Module Documentation

## Project Setup and Installation

### Prerequisites
- Python 3.10 or higher
- Pip package manager
- Git (for cloning the repository)
- Windows, macOS, or Linux operating system

### Installation Steps
1. Clone the repository (if not already done):
   ```bash
   git clone <repository-url>
   cd WildGuard
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure
```
WildGuard/
├── detection/
│   ├── __init__.py        # Package initialization and exports
│   ├── detector.py        # Core detection functionality
│   └── monitor.py         # Real-time directory monitoring
├── test_detection.py      # Test script for detection
├── download_test_image.py # Utility to download test images
├── requirements.txt       # Project dependencies
└── README.md             # Project documentation
```

### File Descriptions

#### detection/detector.py
Core module containing the WildlifeDetector class:
- Handles object detection using YOLOv8
- Processes images and returns detection results
- Provides visualization capabilities

#### detection/monitor.py
Real-time monitoring system:
- Watches directories for new images
- Automatically processes new images
- Saves results to specified output directory

#### detection/__init__.py
Package initialization:
- Exports main classes and functions
- Provides easy access to core functionality

#### test_detection.py
Test script that:
- Downloads a test image if needed
- Runs detection on the image
- Displays results
- Saves annotated image

#### download_test_image.py
Utility script to:
- Download sample images for testing
- Create necessary directories
- Verify downloaded images

#### requirements.txt
Lists all project dependencies:
```
ultralytics==8.0.0
opencv-python==4.11.0.86
watchdog==3.0.0
numpy==1.23.5
pandas==1.5.3
torch==2.0.1
torchvision==0.15.2
```

## How to Run the Project

### 1. Initial Setup
```bash
# Create necessary directories
mkdir input_images output

# Install dependencies
pip install -r requirements.txt
```

### 2. Testing the Detection System
```bash
# Download test image
python download_test_image.py

# Run detection test
python test_detection.py
```

### 3. Real-time Monitoring
```bash
# Create a Python script (e.g., run_monitor.py)
from detection import start_monitoring

start_monitoring(
    watch_dir="input_images",
    output_dir="output"
)

# Run the monitoring script
python run_monitor.py
```

### 4. Using the WildlifeDetector Class
```python
from detection import WildlifeDetector

# Initialize detector
detector = WildlifeDetector()

# Single image detection
image_path = "path/to/image.jpg"
detections = detector.detect(image_path)

# Process results
for det in detections:
    print(f"Detected {det['class']} with confidence {det['confidence']:.2f}")

# Save visualization
detector.draw_detections(
    image_path,
    "output/detected.jpg"
)
```

## Common Usage Scenarios

### 1. Basic Detection
```python
from detection import WildlifeDetector

detector = WildlifeDetector()
results = detector.detect("test.jpg")
print(results)
```

### 2. Continuous Monitoring
```python
from detection import start_monitoring

start_monitoring(
    watch_dir="camera_feed",
    output_dir="alerts"
)
```

### 3. Custom Detection Threshold
```python
detector = WildlifeDetector(confidence=0.7)  # Higher confidence threshold
```

### 4. Batch Processing
```python
import os
from detection import WildlifeDetector

detector = WildlifeDetector()
image_dir = "batch_images"

for image in os.listdir(image_dir):
    if image.endswith(('.jpg', '.png')):
        path = os.path.join(image_dir, image)
        detections = detector.detect(path)
        # Process detections...
```

## Real-Time Video Detection

### Using Webcam Feed
The project includes real-time video detection capabilities through the `video_detection.py` script. This allows you to use your computer's webcam or other connected cameras for live detection.

#### Quick Start (Testing the Video Stream)
1. Make sure your webcam is connected and working
2. Open a terminal in the project directory
3. Run the following command:
   ```bash
   python video_detection.py
   ```
4. You will see:
   - A window titled "WildGuard Detection" opening
   - Your live webcam feed
   - Green boxes around detected objects (people, animals)
   - Labels showing what was detected with confidence scores
   - Processing time in milliseconds (top-left corner)
5. Move around in front of the camera to test detection
6. Press 'q' to quit when done

Expected Performance:
- Initial startup: 2-3 seconds (model loading)
- Detection speed: 10-15 frames per second
- Detection delay: ~90ms per frame
- Memory usage: ~500MB

Troubleshooting Tips:
- If no window appears, try a different camera ID: `python video_detection.py --camera-id 1`
- If detection is slow, reduce resolution: Use `--width 640 --height 480`
- If detection misses objects, lower confidence: `--confidence 0.3`

#### Running Video Detection
```bash
# Start video detection with default webcam
python video_detection.py

# Start with specific camera ID (e.g., external webcam)
python video_detection.py --camera-id 1

# Adjust detection confidence
python video_detection.py --confidence 0.7
```

#### Controls
- Press 'q' to quit the video feed
- Detection results are shown in real-time on the video feed
- Processing time is displayed in the top-left corner

#### Code Example for Custom Video Integration
```python
from detection import WildlifeDetector
import cv2

# Initialize detector
detector = WildlifeDetector(confidence=0.5)

# Setup video capture
cap = cv2.VideoCapture(0)  # Use 0 for default webcam

while True:
    # Read frame
    ret, frame = cap.read()
    if not ret:
        break
        
    # Save frame temporarily
    cv2.imwrite("temp_frame.jpg", frame)
    
    # Get detections
    detections = detector.detect("temp_frame.jpg")
    
    # Draw detections
    for det in detections:
        x1, y1, x2, y2 = map(int, det['bbox'])
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = f"{det['class']} {det['confidence']:.2f}"
        cv2.putText(frame, label, (x1, y1-10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # Display frame
    cv2.imshow('Detection', frame)
    
    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
```

### Performance Considerations
- Real-time video processing requires more computational resources
- Processing speed depends on:
  * CPU/GPU capabilities
  * Frame resolution
  * Number of objects being detected
- Typical performance metrics:
  * ~90ms processing time per frame
  * 10-15 FPS on average CPU
  * Higher FPS possible with GPU acceleration

### Troubleshooting Video Detection

#### Common Issues

1. Camera Access Error
```python
# If default camera doesn't work, try different camera IDs
cap = cv2.VideoCapture(1)  # Try camera ID 1
```

2. Performance Issues
```python
# Reduce frame resolution for better performance
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
```

3. Memory Usage
```python
# Clean up temporary files
import os
os.remove("temp_frame.jpg")  # After processing
```

### Best Practices

1. Frame Rate Control
```python
# Add delay between frames if needed
import time
time.sleep(0.1)  # 100ms delay
```

2. Resource Management
```python
# Proper cleanup
try:
    # Video processing code
finally:
    cap.release()
    cv2.destroyAllWindows()
```

3. Error Handling
```python
if not cap.isOpened():
    print("Error: Could not open camera")
    exit()
```

## Error Handling

### Common Issues and Solutions

1. Import Errors
```
Error: No module named 'ultralytics'
Solution: Run 'pip install -r requirements.txt'
```

2. CUDA Issues
```
Error: CUDA not available
Solution: CPU mode will be used automatically
```

3. Image Loading Errors
```
Error: Image not found
Solution: Verify image path and file existence
```

## Development and Testing

### Running Tests
```bash
# Full test suite
python test_detection.py

# Monitor test
python -c "from detection import start_monitoring; start_monitoring()"
```

### Adding New Features
1. Modify detector.py for new detection capabilities
2. Update monitor.py for new monitoring features
3. Add tests in test_detection.py
4. Update documentation as needed

## Integration with Other Modules

### Connecting with Firebase (Person B)
```python
from detection import WildlifeDetector
# Firebase integration code from Person B
detector = WildlifeDetector()
# Process and send to Firebase...
```

### Mobile App Integration (Person C)
```python
# Detection results are formatted for direct use in mobile app
{
    'class': 'person',
    'confidence': 0.95,
    'bbox': [x1, y1, x2, y2],
    'timestamp': '2025-02-08T15:30:00Z'
}
```

## Monitoring and Maintenance

### Performance Monitoring
- Check processing times in logs
- Monitor memory usage
- Track detection accuracy

### Regular Maintenance
1. Update dependencies monthly
2. Retrain model with new data
3. Review and optimize detection thresholds

This documentation provides a complete guide to setting up, running, and maintaining the AI detection module for WildGuard. For additional support or questions, refer to the project issue tracker.