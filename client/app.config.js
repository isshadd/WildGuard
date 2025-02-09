module.exports = {
  expo: {
    name: "WildGuard",
    slug: "wildguard",
    version: "1.0.0",
    orientation: "portrait",
    icon: "./assets/wildguard.png",
    userInterfaceStyle: "light",
    splash: {
      image: "./assets/wildguard.png",
      resizeMode: "contain",
      backgroundColor: "#ffffff"
    },
    updates: {
      fallbackToCacheTimeout: 0
    },
    assetBundlePatterns: [
      "**/*"
    ],
    ios: {
      supportsTablet: true
    },
    android: {
      adaptiveIcon: {
        foregroundImage: "./assets/wildguard.png",
        backgroundColor: "#FFFFFF"
      }
    },
    web: {
      favicon: "./assets/wildguard.png"
    },
    plugins: [
      [
        "expo-camera",
        {
          cameraPermission: "Allow WildGuard to access your camera."
        }
      ]
    ],
    _internal: {
      isDebug: true
    }
  }
}