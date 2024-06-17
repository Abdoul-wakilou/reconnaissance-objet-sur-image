import tensorflow as tf
import numpy as np
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt
from googletrans import Translator, LANGUAGES

# Charger le modèle pré-entraîné MobileNetV2
model = MobileNetV2(weights='imagenet')

# Initialiser le traducteur
translator = Translator()

def load_and_preprocess_image(img_path):
    # Charger l'image avec la taille de 224x224 pixels
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    # Ajouter une dimension supplémentaire pour le lot (batch)
    img_array = np.expand_dims(img_array, axis=0)
    # Prétraiter l'image comme l'attend MobileNetV2
    img_array = preprocess_input(img_array)
    return img_array

def predict_image(img_path):
    img_array = load_and_preprocess_image(img_path)
    # Faire une prédiction
    predictions = model.predict(img_array)
    # Décoder les prédictions
    decoded_predictions = decode_predictions(predictions, top=5)[0]
    return decoded_predictions

def translate_predictions(predictions):
    translated_predictions = []
    for i, (imagenet_id, label, score) in enumerate(predictions):
        # Assurez-vous que la traduction réussit
        try:
            translated_label = translator.translate(label, src='en', dest='fr').text
        except Exception as e:
            print(f"Erreur de traduction pour {label}: {e}")
            translated_label = label  # Utiliser le label original en cas d'erreur
        translated_predictions.append((imagenet_id, translated_label, score))
    return translated_predictions

def display_image_with_predictions(img_path, predictions):
    # Afficher l'image
    img = image.load_img(img_path)
    plt.imshow(img)
    plt.axis('off')
    
    # Afficher les prédictions traduites
    for i, (imagenet_id, label, score) in enumerate(predictions):
        print(f"{i+1}: {label} ({score*100:.2f}%)")
        plt.text(10, 30 + i * 30, f"{label}: {score*100:.2f}%", color='red', fontsize=12)
    
    plt.show()

# Remplacez 'path/to/your/image.jpg' par le chemin de votre image
image_path = 'responsive.png'
predictions = predict_image(image_path)
translated_predictions = translate_predictions(predictions)
display_image_with_predictions(image_path, translated_predictions)
