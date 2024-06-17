import tensorflow as tf
import numpy as np
import cv2

# Charger le modèle pré-entraîné
model = tf.keras.applications.MobileNetV2(weights='imagenet')

# Charger l'image
image = cv2.imread('profil.jpg')

# Prétraitement de l'image
resized = cv2.resize(image, (224, 224))  # Correction du nom de la fonction
resized = tf.keras.preprocessing.image.img_to_array(resized)
resized = tf.keras.applications.mobilenet_v2.preprocess_input(resized)

# Faire une prédiction
predictions = model.predict(np.array([resized]))
decoded_predictions = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=5)

# Afficher les résultats
for _, label, score in decoded_predictions[0]:
    print(f"Ceci est peut être : {label} avec une probabilité de {score:.2f}")
