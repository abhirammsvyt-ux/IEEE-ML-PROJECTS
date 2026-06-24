# 🩺 Diabetes Risk Prediction Web Application

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://diabetespredictiongit-inql8uanwywdaxkf5wwjnb.streamlit.app)

## 🚀 Live Application

**Access the deployed application here:**

https://diabetespredictiongit-inql8uanwywdaxkf5wwjnb.streamlit.app

---

## 📌 Project Overview

This project was developed as part of the IEEE AI/ML/DL Internship Program.

The application predicts whether a patient is at risk of diabetes using Machine Learning classification techniques based on health parameters provided by the user.

The system accepts the following inputs:

* Number of Pregnancies
* Glucose Level
* Blood Pressure
* Skin Thickness
* Insulin Level
* BMI
* Diabetes Pedigree Function
* Age

The application then provides:

* Diabetes Risk Prediction
* Probability Score
* Risk Level
* Health Recommendations

---

## 🤖 Machine Learning Models

The following models were trained and evaluated:

1. Logistic Regression
2. Random Forest Classifier

### Model Comparison

| Model                    | Accuracy |
| ------------------------ | -------- |
| Logistic Regression      | 76.62%   |
| Random Forest Classifier | 75.97%   |

### Selected Model

**Logistic Regression**

Reason: Achieved the highest accuracy on the test dataset.

---

## 📊 Dataset

Dataset Used:

**Pima Indians Diabetes Dataset**

Features:

* Pregnancies
* Glucose
* BloodPressure
* SkinThickness
* Insulin
* BMI
* DiabetesPedigreeFunction
* Age

Target Variable:

* Outcome (0 = Non-Diabetic, 1 = Diabetic)

---

## 🛠 Technologies Used

* Python
* Streamlit
* Scikit-Learn
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Joblib

---

## 📂 Project Structure

```text
Diabetes_Prediction/
│
├── app.py
├── requirements.txt
│
├── dataset/
│   └── diabetes.csv
│
├── models/
│   ├── diabetes_model.pkl
│   └── scaler.pkl
│
└── notebooks/
    └── diabetes_analysis.ipynb
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone <repository-url>
```

Navigate to the project folder:

```bash
cd Diabetes_Prediction
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

---

## 📷 Application Features

✅ Diabetes Risk Prediction

✅ Probability Score

✅ Risk Meter

✅ BMI Category Analysis

✅ Health Recommendations

✅ Interactive Dashboard

✅ Dark / Light Mode Support

---

## 🎯 Project Outcome

A complete end-to-end Machine Learning solution was developed that:

* Performs diabetes risk prediction.
* Compares multiple classification algorithms.
* Deploys the best-performing model.
* Provides predictions through a professional web application.

---

