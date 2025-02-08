import urllib.request
from pathlib import Path

def download_test_image():
    """Download a test image for the detection system"""
    print("Downloading test image...")
    
    # Create test image directory if it doesn't exist
    Path("test_images").mkdir(exist_ok=True)
    
    # URL of a sample image with a person
    url = "https://raw.githubusercontent.com/ultralytics/yolov5/master/data/images/zidane.jpg"
    output_path = "test.jpg"
    
    try:
        urllib.request.urlretrieve(url, output_path)
        print(f"Test image downloaded successfully to: {output_path}")
    except Exception as e:
        print(f"Error downloading test image: {e}")
        return False
    
    return True

if __name__ == "__main__":
    download_test_image()