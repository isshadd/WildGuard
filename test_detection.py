import os
from pathlib import Path
from detection import WildlifeDetector

def test_detection():
    """Test the wildlife detection system"""
    # Create test directories if they don't exist
    Path("input_images").mkdir(exist_ok=True)
    Path("output").mkdir(exist_ok=True)

    # Initialize detector
    detector = WildlifeDetector()
    
    # Test image path (the one we downloaded earlier)
    test_image = "lion_et_elephant.jpeg"
    output_image = "output/test_detected.jpg"
    
    if not os.path.exists(test_image):
        print(f"Error: Test image {test_image} not found!")
        print("Please run download_test_image.py first.")
        return

    print(f"\nTesting detection on {test_image}...")
    
    try:
        # Run detection
        detections = detector.detect(test_image)
        
        # Print results
        print("\nDetection Results:")
        print("-" * 50)
        if detections:
            for detection in detections:
                print(f"Detected: {detection['class']} with confidence: {detection['confidence']:.2f}")
            
            # Draw detections on image
            if detector.draw_detections(test_image, output_image):
                print("\nAnnotated image saved to:", output_image)
            else:
                print("\nFailed to save annotated image")
        else:
            print("No detections found.")
        print("-" * 50)
        
    except Exception as e:
        print(f"Error during detection: {e}")
        return

if __name__ == "__main__":
    test_detection()