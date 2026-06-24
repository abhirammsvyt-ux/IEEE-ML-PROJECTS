from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import joblib
import os

app = Flask(__name__)

# ── load artefacts (if they exist) ──────────────────────────────────────────
MODEL_DIR = os.path.dirname(__file__)

def load_artifacts():
    try:
        rf_model   = joblib.load(os.path.join(MODEL_DIR, 'salary_model.pkl'))
        le_dict    = joblib.load(os.path.join(MODEL_DIR, 'label_encoders.pkl'))
        feat_names = joblib.load(os.path.join(MODEL_DIR, 'feature_names.pkl'))
        return rf_model, le_dict, feat_names
    except FileNotFoundError:
        return None, None, None

rf_model, le_dict, feat_names = load_artifacts()

# ── helpers ──────────────────────────────────────────────────────────────────
EXPERIENCE_MAP = {
    'EN': 'Entry-level',
    'MI': 'Mid-level',
    'SE': 'Senior',
    'EX': 'Executive / Director',
}
EMPLOYMENT_MAP = {
    'FT': 'Full-time',
    'PT': 'Part-time',
    'CT': 'Contract',
    'FL': 'Freelance',
}
COMPANY_MAP = {
    'S': 'Small  (< 50 employees)',
    'M': 'Medium (50 – 250 employees)',
    'L': 'Large  (> 250 employees)',
}

JOB_TITLES = [
    "3D Computer Vision Researcher", "AI Developer", "AI Programmer",
    "AI Scientist", "Analytics Engineer", "Applied Data Scientist",
    "Applied Machine Learning Scientist", "Applied ML Engineer",
    "Applied Scientist", "Autonomous Vehicle Technician",
    "BI Data Analyst", "Big Data Architect", "Big Data Engineer",
    "Business Data Analyst", "Cloud Data Engineer",
    "Computer Vision Engineer", "Computer Vision Software Engineer",
    "Data Analyst", "Data Analytics Engineer", "Data Analytics Lead",
    "Data Analytics Manager", "Data Architect", "Data DevOps Engineer",
    "Data Engineer", "Data Engineering Manager", "Data Infrastructure Engineer",
    "Data Lead", "Data Manager", "Data Science Consultant",
    "Data Science Engineer", "Data Science Manager",
    "Data Science Tech Lead", "Data Scientist", "Data Specialist",
    "Data Strategist", "Deep Learning Engineer", "Deep Learning Researcher",
    "Director of Data Engineering", "Director of Data Science",
    "ETL Developer", "Finance Data Analyst", "Financial Data Analyst",
    "Head of Data", "Head of Data Science", "Head of Machine Learning",
    "Insights Analyst", "Lead Data Analyst", "Lead Data Engineer",
    "Lead Data Scientist", "Lead Machine Learning Engineer",
    "Machine Learning Developer", "Machine Learning Engineer",
    "Machine Learning Infrastructure Engineer",
    "Machine Learning Manager", "Machine Learning Researcher",
    "Machine Learning Scientist", "Machine Learning Software Engineer",
    "Manager Data Management", "Marketing Data Analyst",
    "ML Engineer", "MLOps Engineer", "NLP Engineer",
    "NLP Scientist", "Principal Data Analyst", "Principal Data Engineer",
    "Principal Data Scientist", "Product Data Analyst",
    "Research Engineer", "Research Scientist", "Software Data Engineer",
    "Staff Data Scientist", "3D Computer Vision Researcher",
]

@app.route('/')
def index():
    return render_template(
        'index.html',
        job_titles=sorted(set(JOB_TITLES)),
        experience_map=EXPERIENCE_MAP,
        employment_map=EMPLOYMENT_MAP,
        company_map=COMPANY_MAP,
        model_ready=(rf_model is not None),
    )

@app.route('/predict', methods=['POST'])
def predict():
    if rf_model is None:
        return jsonify({'error': 'Model not loaded. Please run the notebook first to generate salary_model.pkl.'}), 503

    data = request.get_json()

    try:
        work_year       = int(data['work_year'])
        experience_code = data['experience_level']          # e.g. 'SE'
        employment_code = data['employment_type']           # e.g. 'FT'
        job_title       = data['job_title']
        remote_ratio    = int(data['remote_ratio'])
        company_code    = data['company_size']              # e.g. 'M'

        # encode categoricals
        exp_enc  = le_dict['experience_level'].transform([experience_code])[0]
        emp_enc  = le_dict['employment_type'].transform([employment_code])[0]
        comp_enc = le_dict['company_size'].transform([company_code])[0]

        # job_title: fall back to closest known title if exact match missing
        known_titles = list(le_dict['job_title'].classes_)
        if job_title not in known_titles:
            job_title = 'Data Scientist'   # sensible fallback
        job_enc = le_dict['job_title'].transform([job_title])[0]

        sample = pd.DataFrame([{
            'work_year':        work_year,
            'experience_level': exp_enc,
            'employment_type':  emp_enc,
            'job_title':        job_enc,
            'remote_ratio':     remote_ratio,
            'company_size':     comp_enc,
        }])[feat_names]  # keep column order

        pred = rf_model.predict(sample)[0]

        return jsonify({
            'annual':  round(pred),
            'monthly': round(pred / 12),
            'weekly':  round(pred / 52),
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/health')
def health():
    return jsonify({'model_loaded': rf_model is not None})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
