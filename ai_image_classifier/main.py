import cv2
import numpy as np # comes with tensorflow by default
import streamlit as st
from tensorflow.keras.applications.mobilenet_v2 import (
    MobileNetV2,
    preprocess_input,
    decode_predictions
)
from PIL import Image # come with cv2 by default

def load_model():
    model = MobileNetV2(weights="imagenet")
    return model

def preprocess_image(image):
    img = np.array(image)
    img = cv2.resize(img, (224, 224))
    img = preprocess_input(img)
    img = np.expand_dims(img, axis=0)
    return img

#===========================================================================================================
# TODO 2-5: Classify Image and Decode Predictions
# pass the model a image
# then it gives us back predictions, which is and array of numeric values, [0.34, 0.1, 0.56, ...]
# each value represent a percentage confidence score for each class that the model can predict
# the index of each value corresponds to a specific class label, such as "cat", "dog", "car", etc.
# this means that [0.34, 0.1, 0.56, ...] could mean that 
# the model is 34% confident that the image is a "cat", 10% confident it's a "dog", and 56% confident it's a "car" etc...
# the index of the highest value in the array corresponds to the class that the model thinks the image belongs to
# decode_predictions() function takes these numeric predictions and converts them into human-readable labels
#===========================================================================================================
def classify_image(model, image):
    try:
        processed_image = preprocess_image(image)
        predictions = model.predict(processed_image)

        # takes the numeric prdiction that are genrated by the model and converts them into human-readable labels
        decoded_predictions = decode_predictions(predictions, top=3)[0]# takes the top 3 predictions, ones with the highest confidence scores
        
        return decoded_predictions
    except Exception as e:
        st.error(f"Error classifying image: {str(e)}")
        return None