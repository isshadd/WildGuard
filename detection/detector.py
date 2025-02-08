import cv2
import numpy as np
from ultralytics import YOLO
from typing import List, Dict, Optional

class WildlifeDetector:
    def __init__(self, model_name: str = "yolov8n.pt", confidence: float = 0.55):  # Changed default confidence to 0.55
        """Initialize the detector with a YOLO model"""
        self.confidence = confidence
        try:
            self.model = YOLO(model_name)
            # Store COCO class names
            self.names = {
                0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus',
                6: 'train', 7: 'truck', 8: 'boat', 9: 'traffic light', 10: 'fire hydrant',
                11: 'stop sign', 12: 'parking meter', 13: 'bench', 14: 'bird', 15: 'cat',
                16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant', 21: 'bear',
                22: 'zebra', 23: 'giraffe', 24: 'backpack', 25: 'umbrella', 26: 'handbag',
                27: 'tie', 28: 'suitcase', 29: 'frisbee', 30: 'skis', 31: 'snowboard',
                32: 'sports ball', 33: 'kite', 34: 'baseball bat', 35: 'baseball glove',
                36: 'skateboard', 37: 'surfboard', 38: 'tennis racket', 39: 'bottle',
                40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon',
                45: 'bowl', 46: 'banana', 47: 'apple', 48: 'sandwich', 49: 'orange',
                50: 'broccoli', 51: 'carrot', 52: 'hot dog', 53: 'pizza', 54: 'donut',
                55: 'cake', 56: 'chair', 57: 'couch', 58: 'potted plant', 59: 'bed',
                60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop', 64: 'mouse',
                65: 'remote', 66: 'keyboard', 67: 'cell phone', 68: 'microwave',
                69: 'oven', 70: 'toaster', 71: 'sink', 72: 'refrigerator', 73: 'book',
                74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear',
                78: 'hair drier', 79: 'toothbrush'
            }
        except Exception as e:
            print(f"Error loading model: {e}")
            raise

    def detect(self, image_path: str) -> Optional[List[Dict]]:
        """
        Detect objects in an image
        Returns: List of dictionaries containing detection results
        """
        try:
            print(f"\nProcessing image: {image_path}")
            
            # Run inference
            results = self.model.predict(image_path)
            print(f"Got prediction results: {len(results)} result(s)")
            
            detections = []

            # Get the first result (we only processed one image)
            result = results[0]
            
            # Convert tensor to numpy array
            result_array = result.cpu().numpy()
            print(f"Number of detections: {len(result_array)}")
            
            # Process each detection
            # Each detection is [x1, y1, x2, y2, confidence, class_id]
            for detection in result_array:
                x1, y1, x2, y2, confidence, class_id = detection
                class_id = int(class_id)
                confidence = float(confidence)
                
                print(f"Processing detection: class_id={class_id}, confidence={confidence:.2f}")
                
                # Only filter by confidence threshold
                if confidence >= self.confidence:
                    class_name = self.names.get(class_id, f"unknown_{class_id}")
                    detections.append({
                        'class': class_name,
                        'confidence': confidence,
                        'bbox': [float(x1), float(y1), float(x2), float(y2)]
                    })
                    print(f"Added detection: {class_name} (conf: {confidence:.2f})")
                else:
                    print(f"Skipped detection due to low confidence: {confidence:.2f} < {self.confidence}")

            # Sort detections by confidence (highest first)
            detections.sort(key=lambda x: x['confidence'], reverse=True)
            print(f"Final number of detections: {len(detections)}")
            return detections

        except Exception as e:
            print(f"Error during detection: {e}")
            import traceback
            traceback.print_exc()
            return None

    def draw_detections(self, image_path: str, output_path: str) -> bool:
        """
        Draw detection results on the image and save it
        Returns: True if successful, False otherwise
        """
        try:
            # Get detections
            detections = self.detect(image_path)
            if not detections:
                print("No detections to draw")
                return False

            # Read image
            image = cv2.imread(image_path)
            if image is None:
                print(f"Could not read image: {image_path}")
                return False

            # Draw each detection
            for det in detections:
                x1, y1, x2, y2 = map(int, det['bbox'])
                label = f"{det['class']} {det['confidence']:.2f}"
                
                # Draw bounding box
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                # Draw label
                cv2.putText(image, label, (x1, y1-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Save annotated image
            print(f"Saving annotated image to: {output_path}")
            cv2.imwrite(output_path, image)
            return True

        except Exception as e:
            print(f"Error drawing detections: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    # Simple test
    detector = WildlifeDetector()
    test_image = "test.jpg"
    detections = detector.detect(test_image)
    if detections:
        print(f"Found {len(detections)} objects")
        for det in detections:
            print(f"Detected {det['class']} with confidence {det['confidence']:.2f}")