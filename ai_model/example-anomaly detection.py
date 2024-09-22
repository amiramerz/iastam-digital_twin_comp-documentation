"""An example of an AI anomaly detection code using a simple autoencoder model with Keras . 
This code assumes you are detecting anomalies in a sensor dataset (e.g., temperature, humidity, etc.) collected from the IoT project."""
import numpy as np
import pandas as pd
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# 1. Load Sensor Data
# Assuming the data is stored in a CSV file where each column is a different sensor
data = pd.read_csv('sensor_data.csv')

# 2. Preprocess the Data (Normalize it)
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data)

# 3. Split the Data into Training and Test Sets
# We assume the majority of the training data is non-anomalous (normal operating conditions)
X_train, X_test = train_test_split(data_scaled, test_size=0.2, random_state=42)

# 4. Define the Autoencoder Model
input_dim = X_train.shape[1]  # Number of features (sensors)
encoding_dim = 8  # Size of the encoding layer (bottleneck)

# Input layer
input_layer = Input(shape=(input_dim,))

# Encoding layers
encoded = Dense(16, activation='relu')(input_layer)
encoded = Dense(encoding_dim, activation='relu')(encoded)

# Decoding layers
decoded = Dense(16, activation='relu')(encoded)
decoded = Dense(input_dim, activation='sigmoid')(decoded)

# Define the autoencoder model
autoencoder = Model(inputs=input_layer, outputs=decoded)

# Compile the model
autoencoder.compile(optimizer='adam', loss='mse')

# 5. Train the Autoencoder
history = autoencoder.fit(X_train, X_train,
                          epochs=50,
                          batch_size=32,
                          validation_data=(X_test, X_test),
                          shuffle=True)

# Plot training and validation loss
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.legend()
plt.show()

# 6. Calculate Reconstruction Error on Test Data
X_test_pred = autoencoder.predict(X_test)
reconstruction_error = np.mean(np.power(X_test - X_test_pred, 2), axis=1)

# Plot reconstruction error distribution
plt.hist(reconstruction_error, bins=50)
plt.xlabel('Reconstruction Error')
plt.ylabel('Frequency')
plt.show()

# 7. Set a Threshold for Anomalies
# Any reconstruction error above this threshold will be considered an anomaly
threshold = np.percentile(reconstruction_error, 95)  # Set to the 95th percentile of the error distribution

print(f"Threshold for anomaly detection: {threshold}")

# 8. Detect Anomalies
anomalies = reconstruction_error > threshold

# Print detected anomalies
print(f"Number of anomalies detected: {np.sum(anomalies)}")
anomaly_indices = np.where(anomalies)[0]
print(f"Anomalous data points: {anomaly_indices}")

# Save the model
autoencoder.save('anomaly_detection_autoencoder.h5')
