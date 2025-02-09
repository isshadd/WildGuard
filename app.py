# app.py
import os
import cv2
import time
import numpy as np
from flask import Flask, render_template, Response, request, redirect, url_for
from real_time_detection import analyze_frame  # Votre module de détection en temps réel
from image_detection import detect_poachers     # Votre module de détection sur image
from twilio_notifications import initialize_twilio, notify_all_rangers  # Module pour envoyer les SMS

app = Flask(__name__)

# Configuration du dossier pour sauvegarder les images uploadées
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    """Page d'accueil avec navigation vers la détection en temps réel et l'upload d'image."""
    return render_template('index.html')

@app.route('/video')
def video():
    """Page qui affiche le flux vidéo en temps réel."""
    return render_template('video.html')

def gen_frames():
    """Génère un flux vidéo en temps réel depuis la caméra, avec détection sur chaque frame."""
    cap = cv2.VideoCapture(0)  # 0 = webcam par défaut
    if not cap.isOpened():
        print("Erreur: Impossible d'ouvrir la source vidéo.")
        return

    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            # Analyse de la frame
            message, boxes_info = analyze_frame(frame)
            for (coords, label, conf) in boxes_info:
                x1, y1, x2, y2 = coords.astype(int)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(frame, message, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2, cv2.LINE_AA)
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                continue
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    cap.release()

@app.route('/video_feed')
def video_feed():
    """Endpoint qui fournit le flux vidéo en continu."""
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """
    Page permettant d'uploader une image et d'effectuer l'analyse via le module YOLO.
    Si une détection de "Hunter detected" est renvoyée, une alerte SMS est envoyée.
    """
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            return redirect(request.url)
        if file:
            # Sauvegarde temporaire de l'image
            temp_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(temp_path)
            
            # Upload l'image vers Supabase et obtient l'URL publique
            from backend.utils import upload_image
            public_url = upload_image(temp_path)
            
            # Détection sur l'image
            result = detect_poachers(temp_path)
            
            # Si le résultat indique "Hunter detected", envoyer une alerte SMS
            if "Hunter detected" in result:
                detection_type = "poacher"
                location = {"lat": 45.5017, "lng": -73.5673}  # Coordonnées fictives; adaptez si besoin
                notify_all_rangers(detection_type, public_url, location)
            
            # Supprime le fichier temporaire
            os.remove(temp_path)
            
            return render_template('result.html', result=result, image_url=public_url)
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
    initialize_twilio()  # Initialisation de Twilio pour envoyer les SMS
