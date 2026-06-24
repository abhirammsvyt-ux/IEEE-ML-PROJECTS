# ==============================================================================
# MODEL SCRUBBER UTILITY (Environment Compatibility Fix)
# Made by: Navalrag V P
# 
# Purpose: Resolves Keras serialization/quantization mismatch ("version hell") 
# between the Google Colab training environment and the local Miniconda deployment.
# 
# Note to Evaluators: If you choose to re-train the model in Colab and 
# download the new .keras file, run this utility script on it first before 
# launching the Streamlit app. This strips out incompatible training-specific 
# configurations and guarantees a clean load in the production GUI.
# ==============================================================================

import zipfile
import json
import os

def scrub_model(input_path, output_path):
    # 1. Extract the model zip
    temp_dir = 'temp_extract'
    with zipfile.ZipFile(input_path, 'r') as z:
        z.extractall(temp_dir)
    
    # 2. Scrub the config.json
    config_path = os.path.join(temp_dir, 'config.json')
    with open(config_path, 'r') as f:
        config = json.load(f)

    def remove_tag(obj, tag):
        if isinstance(obj, dict):
            if tag in obj:
                del obj[tag]  # Hard delete the tag
            for k, v in obj.items():
                remove_tag(v, tag)
        elif isinstance(obj, list):
            for item in obj:
                remove_tag(item, tag)

    remove_tag(config, 'quantization_config')
    
    # 3. Save the scrubbed config
    with open(config_path, 'w') as f:
        json.dump(config, f)
        
    # 4. Re-pack the model
    with zipfile.ZipFile(output_path, 'w') as z:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                z.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), temp_dir))
    
    print(f"Success! Scrubbed model saved as: {output_path}")

scrub_model('plant_disease_model.keras', 'scrubbed_model.keras')