import sqlite3
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

# ------------------------------
# 1. Load Data from SQLite Database
# ------------------------------
db_file = "eeg_data.db"
conn = sqlite3.connect(db_file)
query = "SELECT timestamp, alpha_power, beta_power, gamma_power, delta_power, theta_power, action FROM eeg_keypress_log"
data = pd.read_sql_query(query, conn)
conn.close()

# Check the data
print("Data head:")
print(data.head())

# ------------------------------
# 2. Preprocess the Data
# ------------------------------
# Select features (alpha_power and beta_power)
features = data[['alpha_power', 'beta_power', 'gamma_power', 'delta_power', 'theta_power']].values

# Encode the target labels (actions)
# Get unique actions and create a mapping dictionary
actions = data['action'].unique()
action_to_index = {action: idx for idx, action in enumerate(actions)}
print("\nAction mapping:", action_to_index)

# Map the actions to indices
labels = data['action'].map(action_to_index).values

# Convert labels to categorical (one-hot encoding)
labels_categorical = to_categorical(labels)

# Optionally, normalize features (recommended if values vary widely)
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
features = scaler.fit_transform(features)

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    features, labels_categorical, test_size=0.2, random_state=42
)

# ------------------------------
# 3. Build and Train a TensorFlow Model
# ------------------------------
model = Sequential([
    Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    Dense(32, activation='relu'),
    Dense(labels_categorical.shape[1], activation='sigmoid')  # output layer
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

model.summary()

# Train the model
history = model.fit(X_train, y_train,
                    epochs=150,
                    batch_size=16,
                    validation_split=0.2)

# Evaluate on the test set
test_loss, test_acc = model.evaluate(X_test, y_test)
print(f"\nTest accuracy: {test_acc:.2f}")

# ------------------------------
# 4. Save the Trained Model and Scaler
# ------------------------------
# Save the model
model.save("eeg_action_model_tf.keras")
print("\nModel saved to eeg_action_model_tf.keras")

# Save the scaler and mapping dictionary using joblib if needed for later use
import joblib
joblib.dump(scaler, "scaler.pkl")
joblib.dump(action_to_index, "action_to_index.pkl")
print("Scaler and action mapping saved.")
