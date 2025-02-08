# WildGuard - Hackaton Version

**Objectif** : MVP de détection de braconnage en 24h

## Features Retenues
- Détection basique personne/animal (YOLOv8n)
- Notification push Firebase sur app mobile
- Carte interactive avec marqueurs simples
- 3 boutons d'action : 
  ```js
  ['En Route', 'Fausse Alerte', 'Résolu']
  ```

## Architecture Simplifiée
```
[Caméra simulée] -> [IA Python] -> [Firebase] -> [App React Native]
```

## Setup Express

1. **IA** :
```bash
pip install ultralytics opencv-python
python detection/watchdog.py
```

2. **Firebase** :
- Créer projet Firebase
- Activer Firestore + Cloud Messaging
- Copier les clés dans `firebase-config.json`

3. **Mobile** :
```bash
npx react-native init WildGuardApp
cd WildGuardApp && npm install @react-native-firebase/app @react-native-firebase/firestore
```

## Test Scenario
1. Copier `test_image.jpg` dans `input_images/`
2. Vérifier la notification sur smartphone
3. Cliquer "En Route" dans l'app
4. Vérifier la mise à jour Firestore

**Contributors** : [Liste des membres de l'équipe]