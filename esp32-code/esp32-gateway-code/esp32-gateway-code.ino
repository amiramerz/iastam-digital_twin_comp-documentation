#include <WiFi.h>
#include <esp_now.h>
#include <FirebaseESP32.h>

// Firebase credentials
#define FIREBASE_HOST "your-database.firebaseio.com"
#define FIREBASE_AUTH "your-firebase-database-secret"

FirebaseData firebaseData;

// Structure to receive data from room ESP32
typedef struct struct_message {
  float temperature;
  float humidity;
  float light;
  int vibration;
  bool occupancy;
  bool waterLeak;
  bool gasDetected;
  bool intrusion;
} struct_message;

struct_message receivedData;

// Callback function when data is received from the room ESP32
void OnDataReceived(const uint8_t *mac_addr, const uint8_t *data, int len) {
  memcpy(&receivedData, data, sizeof(receivedData));
  
  // Send data to Firebase
  if (Firebase.setInt(firebaseData, "/temperature", receivedData.temperature)) {
      Serial.println("Temperature sent to Firebase");
  }
  if (Firebase.setInt(firebaseData, "/humidity", receivedData.humidity)) {
      Serial.println("Humidity sent to Firebase");
  }
  if (Firebase.setInt(firebaseData, "/light", receivedData.light)) {
      Serial.println("Light level sent to Firebase");
  }
  if (Firebase.setInt(firebaseData, "/vibration", receivedData.vibration)) {
      Serial.println("Vibration sent to Firebase");
  }
  if (Firebase.setBool(firebaseData, "/occupancy", receivedData.occupancy)) {
      Serial.println("Occupancy status sent to Firebase");
  }
  if (Firebase.setBool(firebaseData, "/waterLeak", receivedData.waterLeak)) {
      Serial.println("Water leak status sent to Firebase");
  }
  if (Firebase.setBool(firebaseData, "/gasDetected", receivedData.gasDetected)) {
      Serial.println("Gas detection status sent to Firebase");
  }
  if (Firebase.setBool(firebaseData, "/intrusion", receivedData.intrusion)) {
      Serial.println("Intrusion status sent to Firebase");
  }
}

void setup() {
  Serial.begin(115200);
  
  WiFi.mode(WIFI_STA);
  
  // Initialize Firebase connection
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  
  // Initialize ESP-NOW
  if (esp_now_init() != ESP_OK) {
      Serial.println("Error initializing ESP-NOW");
      return;
  }

  esp_now_register_recv_cb(OnDataReceived);
}

void loop() {
   // No need for additional code in loop as everything is handled in callbacks.
}