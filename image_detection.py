# detect.py

# Importation de la librairie YOLO depuis ultralytics
from ultralytics import YOLO

# Charger le modèle YOLOv8 Nano pré-entraîné (poids déjà téléchargés automatiquement lors de la première utilisation)
model = YOLO('yolov8n.pt')  # Le modèle nano

def detect_poachers(image_path):
    """
    Analyse une image et renvoie un message d'alerte détaillé en fonction des détections.
    Priorités :
      1. S'il y a une détection de "person", renvoyer "Alerte : Braconnier détecté".
      2. Sinon, s'il y a une espèce rare détectée, renvoyer "Attention : espèce rare détectée (<espèce>)".
      3. Sinon, s'il y a d'autres objets détectés, renvoyer "Rien à signaler, je vois un <objet>".
      4. Sinon, renvoyer "RAS".
    """
    results = model(image_path)
    
    # Initialisation des variables de stockage
    person_detected = False
    rare_detections = []   # Liste des tuples (label, confidence)
    other_detections = []  # Liste des tuples (label, confidence)
    
    # Liste des espèces rares à surveiller
    
    # Liste des espèces rares à surveiller
    rare_species = ["zebra", "rhino", "elephant"]  # modifiez cette liste selon vos besoins

    # Parcourir toutes les détections du modèle
    for box in results[0].boxes:
        class_id = int(box.cls)              # ID de la classe détectée
        label = model.names[class_id]        # Nom de la classe
        conf = float(box.conf)               # Confiance associée à la détection
        
        if label == "person":
            person_detected = True
        elif label in rare_species:
            rare_detections.append((label, conf))
        else:
            other_detections.append((label, conf))
    
    # Priorité 1 : Braconnier (personne détectée)
    if person_detected:
        return "----- ALERT : Hunter detected ! -----"
    
    # Priorité 2 : Espèce rare détectée
    if rare_detections:
        # Choisir la détection rare avec la confiance la plus élevée
        best_rare = max(rare_detections, key=lambda x: x[1])
        return f"-- WARNING : Rare specie detected : {best_rare[0]} ! --"
    
    # Priorité 3 : Autres détections
    if other_detections:
        # Choisir la détection avec la confiance la plus élevée parmi les autres
        best_other = max(other_detections, key=lambda x: x[1])
        return f"- Nothing special to report, I see a {best_other[0]} -"
    
    # Aucun objet détecté
    return "Nothing to report, RAS"


# Bloc principal pour tester la fonction
if __name__ == '__main__':
    # Remplacez 'chemin/vers/image.jpg' par le chemin réel de l'image à tester
    test_image = "images/elephant.jpeg"  # Par exemple, une image téléchargée sur Google "chasseur photo"
    result = detect_poachers(test_image)
    print(result)
