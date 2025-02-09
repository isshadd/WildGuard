import cv2
import time
import numpy as np
from PytorchWildlife.models import detection as pw_detection
from PytorchWildlife.models import classification as pw_classification

# Instanciation du modèle de détection MegaDetectorV6
detection_model = pw_detection.MegaDetectorV6(version="MDV6-yolov10-c")
# Instanciation du modèle de classification (par exemple, AI4GAmazonRainforest)
classification_model = pw_classification.AI4GAmazonRainforest()

# Mapping des classes tel que renvoyé par MegaDetectorV6 (0-indexé)
mega_mapping = {
    0: "animal",
    1: "person",
    2: "vehicle"
}

# Ensemble des espèces rares
RARE_ANIMAL_CLASSES = {
    "elephant", "rhino", "lion", "leopard", "cheetah",
    "giraffe", "zebra", "hippo", "buffalo", "crocodile",
    "gorilla", "chimpanzee", "bonobo", "orangutan",
    "tiger", "panda", "koala", "penguin", "polar bear",
    "jaguar", "snow leopard", "lynx", "ocelot", "serval"
}

VEHICLE_CLASSES = {"vehicle"}

def analyze_frame(frame):
    """
    Analyse une frame et retourne :
      - Un message d'alerte selon la priorité :
           1. Person
           2. Rare animal (ex. elephant, rhino, lion, etc.)
           3. Autre animal (espèce classifiée)
           4. Vehicle
      - Une liste d'informations pour dessiner les bounding boxes sous la forme :
           (coords, label, confidence)
         où coords est un tableau numpy [x1, y1, x2, y2].
    """
    results = detection_model.predictor(frame)
    
    person_detected = False
    rare_animal_detections = []  # Liste de tuples (label, confidence)
    animal_detections = []       # Liste de tuples (label, confidence)
    vehicle_detections = []      # Liste de tuples (label, confidence)
    boxes_info = []              # Pour stocker (coords, label, confidence)
    
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls)
            conf = float(box.conf)
            base_label = mega_mapping.get(class_id, str(class_id))
            coords = box.xyxy[0].cpu().numpy()
            label = base_label  # Par défaut
            
            # Si la détection est "animal", on essaie de classer l'espèce
            if base_label == "animal":
                x1, y1, x2, y2 = coords.astype(int)
                h, w, _ = frame.shape
                x1, y1 = max(0, x1), max(0, y1)
                x2, y2 = min(w, x2), min(h, y2)
                if x2 > x1 and y2 > y1:
                    crop = frame[y1:y2, x1:x2]
                    if crop.ndim == 3 and crop.shape[2] == 3:
                        try:
                            print("Crop shape before conversion:", crop.shape)
                            crop_rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
                            # Ici, on passe directement le crop en uint8 (format attendu par PIL)
                            species_result = classification_model.single_image_classification(crop_rgb)
                            # Récupérer le champ "prediction" (par exemple "Leopardus")
                            species_label = species_result.get("prediction", "animal")
                            label = species_label  # Mise à jour du label avec l'espèce détectée
                        except Exception as e:
                            print("Classification error:", e)
                    else:
                        print("Invalid crop shape:", crop.shape)
            
            boxes_info.append((coords, label, conf))
            
            if label == "person":
                person_detected = True
            elif label in VEHICLE_CLASSES:
                vehicle_detections.append((label, conf))
            else:
                if label in RARE_ANIMAL_CLASSES:
                    rare_animal_detections.append((label, conf))
                else:
                    animal_detections.append((label, conf))
    
    if person_detected:
        message = "ALERT: Person detected!"
    elif rare_animal_detections:
        best_rare = max(rare_animal_detections, key=lambda x: x[1])
        message = f"WARNING: Rare animal detected ({best_rare[0]})"
    elif animal_detections:
        best_animal = max(animal_detections, key=lambda x: x[1])
        message = f"Attention: Animal detected ({best_animal[0]})"
    elif vehicle_detections:
        best_vehicle = max(vehicle_detections, key=lambda x: x[1])
        message = f"Notice: Vehicle detected ({best_vehicle[0]})"
    else:
        message = "Nothing to report."
    
    return message, boxes_info

def detect_video(video_source=0):
    """
    Capture une vidéo en temps réel et effectue une détection.
    Appuyez sur 'q' pour quitter.
    """
    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print("Error: Cannot open video source.")
        return
    
    prev_time = time.time()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time
        
        message, boxes_info = analyze_frame(frame)
        
        for (coords, label, conf) in boxes_info:
            x1, y1, x2, y2 = coords.astype(int)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        cv2.putText(frame, message, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (0, 255, 0), 2)
        
        cv2.imshow("Real-Time Video Detection", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    detect_video(0)
