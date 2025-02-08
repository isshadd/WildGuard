import os
from firebase_admin import storage

def upload_image(image_path, destination_folder="alertes"):
    bucket = storage.bucket()
    """
    Upload une image vers Cloud Storage et retourne l'URL publique.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Fichier non trouvé: {image_path}")

    # Extraire le nom de fichier
    file_name = os.path.basename(image_path)
    destination_path = f"{destination_folder}/{file_name}"

    blob = bucket.blob(destination_path)
    blob.upload_from_filename(image_path)
    
    # Rendre l'image publique (optionnel : à ajuster selon vos règles de sécurité)
    blob.make_public()
    return blob.public_url

from firebase_admin import firestore
from datetime import datetime

def send_alert(image_path, detection_label):
    db = firestore.client()
    """
    Enregistre une alerte dans Firestore avec l'URL de l'image, le type de détection et le timestamp.
    """
    # Upload de l'image et récupération de l'URL
    try:
        image_url = upload_image(image_path)
    except Exception as e:
        print(f"Erreur lors de l'upload de l'image : {e}")
        return

    alert_data = {
        "type": detection_label,          # Exemple : "braconnier" ou "espèce rare"
        "image_url": image_url,
        "timestamp": datetime.utcnow()
    }

    db.collection("alertes").add(alert_data)
    print("Alerte envoyée:", alert_data)
