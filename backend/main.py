import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from utils import send_alert, get_recent_alerts, update_alert_status

class ImageWatcher(FileSystemEventHandler):
    def on_created(self, event):
        """Handle new image file creation"""
        if event.is_directory:
            return
        
        # Check if the created file is an image
        if event.src_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            print(f"New image detected: {event.src_path}")
            self.process_image(event.src_path)
    
    def process_image(self, image_path):
        """
        Process a new image and send alert if needed.
        For the hackathon demo, we'll simulate AI detection based on filename.
        In production, this would integrate with Person A's AI model.
        """
        try:
            # Simulate AI detection based on filename
            filename = os.path.basename(image_path).lower()
            
            # Check for specific animals or threats in filename
            if 'elephant' in filename:
                detection_label = 'endangered_species'
                species_type = 'elephant'
                print(f"Detected endangered species: {species_type}")
            elif any(animal in filename for animal in ['tiger', 'rhino', 'leopard']):
                detection_label = 'endangered_species'
                species_type = next(animal for animal in ['tiger', 'rhino', 'leopard'] if animal in filename)
                print(f"Detected endangered species: {species_type}")
            elif 'poacher' in filename or 'threat' in filename or 'person' in filename:
                detection_label = 'poacher'
                print("Detected potential threat: possible poacher")
            else:
                print("No significant detection in image")
                return
            
            # Simulate GPS coordinates (in production, would come from camera metadata)
            mock_location = {
                "lat": 45.5017,  # Montreal's approximate latitude
                "lng": -73.5673  # Montreal's approximate longitude
            }
            
            print(f"Processing {detection_label} detection...")
            
            # Send alert to cloud storage and database
            alert_id = send_alert(
                image_path=image_path,
                detection_label=detection_label,
                location=mock_location
            )
            
            print(f"Alert sent successfully! Alert ID: {alert_id}")
            
        except Exception as e:
            print(f"Error processing image: {e}")

def start_watching(input_dir="input_images"):
    """
    Start watching a directory for new images.
    """
    # Create input directory if it doesn't exist
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
        print(f"Created input directory: {input_dir}")
    
    # Set up watchdog observer
    event_handler = ImageWatcher()
    observer = Observer()
    observer.schedule(event_handler, input_dir, recursive=False)
    observer.start()
    
    print(f"\nWildGuard Backend Service")
    print(f"-------------------------")
    print(f"Watching directory '{input_dir}' for new images")
    print("Supported formats: .jpg, .jpeg, .png")
    print("\nDetection triggers:")
    print("- Endangered species: filenames containing 'elephant', 'tiger', 'rhino', 'leopard'")
    print("- Potential threats: filenames containing 'poacher', 'threat', 'person'")
    print("\nPress Ctrl+C to stop the service")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nStopping WildGuard service...")
    
    observer.join()

def test_system():
    """Test the alert system with test images"""
    print("\nWildGuard Alert System Test")
    print("-------------------------")
    
    test_dir = "test_images"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
        print(f"Created test directory: {test_dir}")
        print("Please add test images to the test_images directory")
        return
    
    # Find test images
    test_images = [f for f in os.listdir(test_dir) 
                  if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    if not test_images:
        print("No test images found in test_images directory")
        print("Please add some .jpg, .jpeg, or .png files for testing")
        return
    
    print(f"Found {len(test_images)} test images")
    for image in test_images:
        try:
            image_path = os.path.join(test_dir, image)
            print(f"\nTesting with image: {image}")
            
            # Process the test image
            handler = ImageWatcher()
            handler.process_image(image_path)
            
        except Exception as e:
            print(f"Test failed for {image}: {e}")
    
    # Show recent alerts
    try:
        print("\nRecent Alerts (Montreal Time):")
        print("-----------------------------")
        alerts = get_recent_alerts(limit=5)
        for alert in alerts:
            alert_type = alert['type'].replace('_', ' ').title()
            created_at = alert['created_at']
            print(f"➜ {alert_type} detected at {created_at}")
    except Exception as e:
        print(f"Error retrieving recent alerts: {e}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="WildGuard Backend Service")
    parser.add_argument("--test", action="store_true", help="Run system test")
    parser.add_argument("--input-dir", default="input_images", 
                       help="Directory to watch for new images")
    
    args = parser.parse_args()
    
    if args.test:
        test_system()
    else:
        start_watching(args.input_dir)
