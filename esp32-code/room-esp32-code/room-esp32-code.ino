#include <WiFi.h>
#include <esp_now.h>
#include <DHT.h>
#include <BH1750.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>

// Define sensor pins and types
#define DHTPIN 4
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);
BH1750 lightSensor;
Adafruit_ADXL345_U adxl = Adafruit_ADXL345_U(12345);

// Structure to hold sensor data
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

struct_message sensorData;

// Callback when data is sent successfully
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
    Serial.println("Data sent successfully");
}

void setup() {
    Serial.begin(115200);
    dht.begin();
    lightSensor.begin();
    adxl.begin();
    
    // Initialize ESP-NOW
    if (esp_now_init() != ESP_OK) {
        Serial.println("Error initializing ESP-NOW");
        return;
    }
    
    esp_now_register_send_cb(OnDataSent);
    
    // Define peer (central ESP32)
    esp_now_peer_info_t peerInfo;
    memcpy(peerInfo.peer_addr, centralESP32_MAC, 6); // Replace with central MAC address
    peerInfo.channel = 0;  
    peerInfo.encrypt = false;

    if (esp_now_add_peer(&peerInfo) != ESP_OK) {
        Serial.println("Failed to add peer");
        return;
    }
}

void loop() {
    // Read sensors
    sensorData.temperature = dht.readTemperature();
    sensorData.humidity = dht.readHumidity();
    
    uint16_t lux = lightSensor.readLightLevel();
    sensorData.light = lux;

    sensors_event_t event; 
    adxl.getEvent(&event);
    sensorData.vibration = event.acceleration.x; // Example usage

    // Simulated readings for other sensors
    sensorData.occupancy = digitalRead(occupancySensorPin); // Example pin setup
    sensorData.waterLeak = digitalRead(waterLeakSensorPin); // Example pin setup
    sensorData.gasDetected = digitalRead(gasSensorPin); // Example pin setup
    sensorData.intrusion = digitalRead(intrusionSensorPin); // Example pin setup

    // Send data to central ESP32
    esp_err_t result = esp_now_send(centralESP32_MAC, (uint8_t *)&sensorData, sizeof(sensorData));
    
    if (result == ESP_OK) {
        Serial.println("Sent with success");
    } else {
        Serial.println("Error sending data");
    }

    delay(10000); // Send data every 10 seconds
}

