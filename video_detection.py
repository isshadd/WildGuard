import cv2
from detection import WildlifeDetector
import time
import argparse

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='WildGuard Real-time Video Detection')
    parser.add_argument('--camera-id', type=int, default=0,
                      help='Camera device ID (default: 0)')
    parser.add_argument('--confidence', type=float, default=0.5,
                      help='Detection confidence threshold (0-1)')
    parser.add_argument('--width', type=int, default=1280,
                      help='Camera resolution width')
    parser.add_argument('--height', type=int, default=720,
                      help='Camera resolution height')
    return parser.parse_args()

def start_video_detection(camera_id=0, confidence=0.5, width=1280, height=720):
    """
    Run real-time detection on video feed from camera
    
    Args:
        camera_id: Camera device ID (default is 0 for primary webcam)
        confidence: Detection confidence threshold (0-1)
        width: Camera capture width resolution
        height: Camera capture height resolution
    """
    print(f"\nStarting WildGuard Video Detection...")
    print(f"Camera ID: {camera_id}")
    print(f"Confidence Threshold: {confidence}")
    print(f"Resolution: {width}x{height}")
    print("\nInitializing detector...")
    
    # Initialize detector
    detector = WildlifeDetector(confidence=confidence)
    
    # Initialize video capture
    cap = cv2.VideoCapture(camera_id)
    
    if not cap.isOpened():
        print(f"Error: Could not open camera (ID: {camera_id})")
        return
    
    # Set resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    
    # Get actual video properties (might differ from requested)
    actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    print(f"Camera initialized: {actual_width}x{actual_height} @ {fps}fps")
    print("Press 'q' to quit")
    
    try:
        frame_count = 0
        start_time = time.time()
        
        while True:
            # Read frame from camera
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame")
                break
            
            # Save frame temporarily
            temp_path = "temp_frame.jpg"
            cv2.imwrite(temp_path, frame)
            
            # Get detections
            process_start = time.time()
            detections = detector.detect(temp_path)
            process_time = (time.time() - process_start) * 1000  # Convert to ms
            
            # Draw detections on frame
            if detections:
                for det in detections:
                    # Get coordinates
                    x1, y1, x2, y2 = map(int, det['bbox'])
                    
                    # Draw bounding box
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    
                    # Draw label with confidence
                    label = f"{det['class']} {det['confidence']:.2f}"
                    cv2.putText(frame, label, (x1, y1-10),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # Calculate FPS
            frame_count += 1
            elapsed_time = time.time() - start_time
            fps = frame_count / elapsed_time
            
            # Draw performance info
            cv2.putText(frame, f"Process: {process_time:.1f}ms FPS: {fps:.1f}",
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Show frame
            cv2.imshow('WildGuard Detection', frame)
            
            # Check for 'q' key to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("\nStopping detection...")
                break
                
    except KeyboardInterrupt:
        print("\nStopping detection...")
    
    finally:
        # Clean up
        cap.release()
        cv2.destroyAllWindows()
        
        # Print session stats
        print(f"\nSession Statistics:")
        print(f"Total Frames: {frame_count}")
        print(f"Average FPS: {frame_count/elapsed_time:.1f}")
        print(f"Total Time: {elapsed_time:.1f} seconds")

if __name__ == "__main__":
    args = parse_args()
    start_video_detection(
        camera_id=args.camera_id,
        confidence=args.confidence,
        width=args.width,
        height=args.height
    )