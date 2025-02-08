import os
import time
from pathlib import Path
from typing import Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .detector import WildlifeDetector

class ImageProcessor:
    def __init__(self, output_dir: str = "output"):
        self.detector = WildlifeDetector()
        self.output_dir = output_dir
        Path(output_dir).mkdir(exist_ok=True)

    def process_image(self, image_path: str) -> Optional[dict]:
        """Process a single image and return detection results"""
        try:
            result = self.detector.detect(image_path)
            if result:
                self._save_result(image_path, result)
            return result
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")
            return None

    def _save_result(self, image_path: str, result: dict):
        """Save detection results"""
        base_name = os.path.basename(image_path)
        output_path = os.path.join(self.output_dir, f"result_{base_name}.txt")
        with open(output_path, 'w') as f:
            f.write(str(result))

class ImageWatchdog(FileSystemEventHandler):
    def __init__(self, processor: ImageProcessor):
        self.processor = processor

    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith(('.jpg', '.jpeg', '.png')):
            print(f"New image detected: {event.src_path}")
            self.processor.process_image(event.src_path)

def start_monitoring(watch_dir: str = "input_images", output_dir: str = "output"):
    """Start monitoring a directory for new images"""
    processor = ImageProcessor(output_dir)
    event_handler = ImageWatchdog(processor)
    observer = Observer()
    observer.schedule(event_handler, watch_dir, recursive=False)
    observer.start()

    try:
        print(f"Started monitoring {watch_dir} for new images...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nMonitoring stopped.")
    
    observer.join()

if __name__ == "__main__":
    start_monitoring()