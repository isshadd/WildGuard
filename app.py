# app.py
import os
import cv2
import time
import numpy as np
from flask import Flask, render_template, Response, request, redirect, url_for
from real_time_detection import analyze_frame  # Importez la fonction d'analyse du module temps réel
from image_detection import detect_poachers     # Importez la fonction de détection sur image

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
app = Flask(__name__, template_folder=TEMPLATE_DIR)

# Pour stocker les images uploadées dans le dossier static/uploads
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route('/')
def index():
    """Page d'accueil avec navigation vers la détection en temps réel et l'upload d'image."""
    return render_template('index.html')


@app.route('/video')
def video():
    """Page qui intègre le flux vidéo en temps réel."""
    return render_template('video.html')


def gen_frames():
    """Générateur de frames pour le streaming vidéo.
    Capture les images depuis la caméra, applique l'analyse et retourne des frames JPEG."""
    cap = cv2.VideoCapture(0)  # 0 = webcam par défaut (modifiez selon votre configuration)
    if not cap.isOpened():
        print("Erreur: Impossible d'ouvrir la source vidéo.")
        return

    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            # Analyse de la frame via le module real_time_detection
            message, boxes_info = analyze_frame(frame)

            # Dessiner les bounding boxes et les labels sur la frame
            for (coords, label, conf) in boxes_info:
                x1, y1, x2, y2 = coords.astype(int)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(frame, message, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2, cv2.LINE_AA)

            # Encodage de la frame en JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                continue
            frame = buffer.tobytes()

            # Renvoi de la frame dans le format multipart requis pour le streaming
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
    """Page pour uploader une image et effectuer l'analyse avec le module YOLO."""
    if request.method == 'POST':
        # Vérifie si le champ 'image' existe dans le formulaire
        if 'image' not in request.files:
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            return redirect(request.url)
        if file:
            # Sauvegarde de l'image dans le dossier uploads
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            # Appel de la fonction de détection sur image
            result = detect_poachers(file_path)
            # Affiche le résultat
            return render_template('result.html', result=result, image_url=file.filename)
    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)
