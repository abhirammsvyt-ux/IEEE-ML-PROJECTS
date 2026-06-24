``markdown
# 🌿 Deep Learning Plant Disease Detector

A deep learning web application that identifies **plant diseases from leaf images** using a trained Convolutional Neural Network (CNN).

## 📌 Project Overview
Developed as part of the **IEEE AI/ML/DL Internship Program**.
Upload a photo of a plant leaf and the app instantly diagnoses the disease and provides treatment recommendations.

## ✨ Features
- 🖼️ Upload leaf images (JPG / PNG)
- 🔍 Real-time CNN-based disease classification
- 📋 Disease description and treatment suggestions
- 🌱 Supports multiple plant species and disease categories

## 🤖 Model
| Detail | Info |
|---|---|
| Architecture | Convolutional Neural Network (CNN) |
| Framework | TensorFlow / Keras |
| Model file | `scrubbed_model.keras` (~43MB) |
| Format | Sanitized Keras model (safe for deployment) |

## 🗂️ Project Structure
```
Plant_Disease_Detection/
├── app.py                   # Streamlit web application
├── data.py                  # Disease info & treatment database
├── scrub_model.py           # Model sanitization script
├── scrubbed_model.keras     # Trained CNN model
└── how_to_run.txt           # Detailed local setup instructions
```

## 🛠️ Tech Stack
`Python 3.10` · `TensorFlow` · `Keras` · `Streamlit` · `Pillow` · `NumPy` · `Conda`

## ⚙️ How to Run

> ⚠️ Use **Miniconda or Anaconda** to avoid dependency conflicts.

```bash
# 1. Create a dedicated environment
conda create -n plant_env python=3.10 -y
conda activate plant_env

# 2. Clone the repository
git clone https://github.com/abhirammsvyt-ux/IEEE-ML-PROJECTS.git
cd IEEE-ML-Projects/Plant_Disease_Detection

# 3. Install dependencies
pip install tensorflow streamlit pillow numpy

# 4. Launch the app
streamlit run app.py
```

The app opens at **http://localhost:8501**
```

Commit message:
```
Add Plant Disease Detection README
```

---
