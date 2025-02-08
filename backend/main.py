import firebase_admin
from firebase_admin import credentials, firestore, storage

# Initialisation de Firebase avec la clé de service
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'WildGuard.appspot.com'  # Remplacez par le nom de votre bucket
})

# Accès aux services
db = firestore.client()
bucket = storage.bucket()
