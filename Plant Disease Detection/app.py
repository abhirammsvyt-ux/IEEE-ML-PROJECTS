import streamlit as st
import numpy as np
from PIL import Image
from data import DISEASE_INFO
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.layers import Dense

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Plant Disease Detection", page_icon="🌿", layout="wide")

# --- "GHOST PATCH" CLASS ---
# This intercepts the 'Dense' layer loading and ignores the 'quantization_config' error
class PatchedDense(Dense):
    def __init__(self, **kwargs):
        if 'quantization_config' in kwargs:
            kwargs.pop('quantization_config')
        super().__init__(**kwargs)

# --- LOAD CACHED MODEL ---
@st.cache_resource
def load_keras_model():
    # Load the scrubbed, sanitized model
    return load_model('scrubbed_model.keras', compile=False, safe_mode=False)

model = load_keras_model()

# --- MAIN UI ---
st.title("🌿 Deep Learning Plant Disease Detector")
uploaded_file = st.file_uploader("Choose a leaf image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Uploaded Image")
        # .convert('RGB') is the critical fix for the alpha channel
        image = Image.open(uploaded_file).convert('RGB') 
        st.image(image, use_column_width=True)

    with st.spinner("Analyzing..."):
        img_resized = image.resize((256, 256)) 
        img_array = img_to_array(img_resized)
        img_array = np.expand_dims(img_array, axis=0)
        
        # TACTICAL FIX: Disabled double-scaling. The model already handles this internally.
        # img_array = img_array / 255.0  

        predictions = model.predict(img_array)
        predicted_class_index = np.argmax(predictions, axis=1)[0]
        confidence_score = np.max(predictions) * 100

    with col2:
        st.subheader("Diagnostic Results")
        disease_data = DISEASE_INFO.get(predicted_class_index, {"name": "Unknown", "description": "N/A", "symptoms": "N/A", "prevention": "N/A"})
        
        # Display the high-level metric
        st.metric(label="Predicted Condition", value=disease_data["name"], delta=f"{confidence_score:.2f}% Confidence")
        
        # Display the extra info from data.py
        st.write("---")
        st.write(f"**Description:** {disease_data['description']}")
        st.write(f"**Symptoms:** {disease_data['symptoms']}")
        st.write(f"**Prevention:** {disease_data['prevention']}")