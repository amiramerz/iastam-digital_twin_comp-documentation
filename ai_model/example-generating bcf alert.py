"""To integrate the Building Collaboration Format (BCF) into the AI anomaly detection code, we will follow these steps:

Detect Anomalies: Use your anomaly detection model to identify anomalies in the sensor data.
Create BCF Alerts: When an anomaly is detected, generate a BCF file that contains the relevant details.
Save or Send the BCF File: Store the BCF file in a desired location or send it to a BIM system for integration."""
import json
import os

# Sample anomaly detection function (replace with your AI model logic)
def detect_anomalies(sensor_data):
    anomalies = []
    threshold = 0.5  # Example threshold for anomaly detection
    for data_point in sensor_data:
        reconstruction_error = calculate_reconstruction_error(data_point)
        if reconstruction_error > threshold:
            anomalies.append(data_point)
    return anomalies

# Function to calculate reconstruction error (placeholder)
def calculate_reconstruction_error(data_point):
    # Placeholder for actual reconstruction logic
    return abs(data_point - 0.5)  # Example calculation

# Function to create BCF format alert
def create_bcf_alert(anomaly):
    bcf_alert = {
        "projectId": "YourProjectID",
        "topic": "Anomaly Detection",
        "status": "Open",
        "creationDate": "2024-09-22T12:00:00Z",  # Example timestamp
        "viewpoint": {
            "cameraView": {
                "position": {"x": 0, "y": 0, "z": 0},
                "target": {"x": 0, "y": 0, "z": 1},
                "up": {"x": 0, "y": 1, "z": 0}
            }
        },
        "guid": "unique-alert-id",  # Generate a unique ID
        "description": f"Anomaly detected: {anomaly}",
        "severity": "High"
    }
    return bcf_alert

# Function to save BCF alert to a file
def save_bcf_alert(bcf_alert, file_path):
    with open(file_path, 'a') as file:
        json.dump(bcf_alert, file)
        file.write("\n")  # New line for each alert

# Main logic
sensor_data = [0.1, 0.3, 0.8, 0.6]  # Example sensor data
anomalies = detect_anomalies(sensor_data)

for anomaly in anomalies:
    bcf_alert = create_bcf_alert(anomaly)
    save_bcf_alert(bcf_alert, "bcf_alerts.json")  # Save to JSON file
