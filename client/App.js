import React, { useState, useEffect, useRef } from 'react';
import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View, Button, Image, Alert } from 'react-native';
import { Camera } from 'expo-camera';
import * as ImagePicker from 'expo-image-picker';

export default function App() {
  // 'home' = écran d'accueil, 'live' = détection en temps réel, 'image' = analyse d'image
  const [mode, setMode] = useState('home');

  // Pour le mode live camera
  const [hasCameraPermission, setHasCameraPermission] = useState(null);
  const [cameraRef, setCameraRef] = useState(null);
  const [alertMessage, setAlertMessage] = useState('');

  // Pour le mode image analysis
  const [selectedImage, setSelectedImage] = useState(null);
  const [analysisResult, setAnalysisResult] = useState('');

  // Demande des permissions pour la caméra
  useEffect(() => {
    (async () => {
      const { status } = await Camera.requestCameraPermissionsAsync();
      setHasCameraPermission(status === 'granted');
    })();
  }, []);

  // Fonction de détection en temps réel (simulation)
  const handleLiveDetection = async () => {
    if (cameraRef) {
      const photo = await cameraRef.takePictureAsync();
      // Ici, vous enverriez 'photo' à votre backend Python
      // Simulation d'analyse :
      const mockDetection =
        Math.random() > 0.5
          ? "ALERT: Person detected!"
          : "WARNING: Rare animal detected (lion)";
      setAlertMessage(mockDetection);
      Alert.alert('Detection Alert', mockDetection);
    }
  };

  // Fonction de sélection d'image et simulation d'analyse
  const handlePickImage = async () => {
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      quality: 1,
    });
    if (!result.canceled) {
      setSelectedImage(result.assets[0].uri);
      // Simulation d'analyse :
      const mockResult =
        Math.random() > 0.5
          ? "ALERT: Hunter detected!"
          : "WARNING: Rare specie detected: elephant!";
      setAnalysisResult(mockResult);
    }
  };

  // Écran d'accueil
  if (mode === 'home') {
    return (
      <View style={styles.container}>
        <Text style={styles.title}>WildGuard</Text>
        <Button title="Live Camera" onPress={() => setMode('live')} />
        <Button title="Image Analysis" onPress={() => setMode('image')} />
        <StatusBar style="auto" />
      </View>
    );
  }

  // Mode détection en temps réel (live camera)
  if (mode === 'live') {
    if (hasCameraPermission === false) {
      return <Text>No camera access</Text>;
    }
    return (
      <View style={styles.container}>
        <Camera style={styles.camera} ref={ref => setCameraRef(ref)}>
          <View style={styles.alertBox}>
            <Text style={styles.alertText}>{alertMessage}</Text>
          </View>
        </Camera>
        <Button title="Analyze Frame" onPress={handleLiveDetection} />
        <Button title="Back Home" onPress={() => setMode('home')} />
        <StatusBar style="auto" />
      </View>
    );
  }

  // Mode analyse d'image
  if (mode === 'image') {
    return (
      <View style={styles.container}>
        <Button title="Select Image" onPress={handlePickImage} />
        {selectedImage && (
          <>
            <Image source={{ uri: selectedImage }} style={styles.image} />
            <Text style={styles.resultText}>{analysisResult}</Text>
          </>
        )}
        <Button title="Back Home" onPress={() => setMode('home')} />
        <StatusBar style="auto" />
      </View>
    );
  }

  return null;
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  camera: {
    width: '100%',
    height: '70%',
  },
  alertBox: {
    position: 'absolute',
    top: 20,
    backgroundColor: 'rgba(255,0,0,0.7)',
    padding: 10,
    borderRadius: 5,
  },
  alertText: {
    color: 'white',
    fontWeight: 'bold',
  },
  image: {
    width: 300,
    height: 300,
    marginVertical: 20,
  },
  resultText: {
    fontSize: 20,
    color: 'red',
    fontWeight: 'bold',
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    marginBottom: 20,
  },
});
