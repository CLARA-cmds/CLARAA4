from flask import Flask, request, render_template, jsonify
import numpy as np
import joblib
import pandas as pd

app = Flask(__name__)

# Load the trained model
model = joblib.load("CS_model.pkl")

# Load training dataset to get correct min-max values for normalization
df = pd.read_excel("train.xlsx", sheet_name="Sheet1")

# Clean column names
df.columns = (
    df.columns.str.replace(r"[^a-zA-Z0-9_]", "", regex=True)
    .str.replace(" ", "_")
)

# Extract feature names used in training
feature_columns = [col for col in df.columns if col != "Cancer_Stage"]

# Function to normalize input data
def preprocess_input(data):
    data_df = pd.DataFrame([data], columns=feature_columns)
    
    # Apply the same min-max scaling used during training
    for col in feature_columns:
        data_df[col] = (data_df[col] - df[col].min()) / (df[col].max() - df[col].min())
    
    return data_df

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    features = data["inputs"]  # List of feature values
    
    # Ensure proper feature order and normalization
    normalized_features = preprocess_input(features)
    
    # Predict the cancer stage
    prediction = model.predict(normalized_features)
    
    return jsonify({"stage": int(prediction[0])})

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/screenAu")
def screen_au():
    return render_template("screenAu.html")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5050))
    app.run(debug=False, host="0.0.0.0", port=port)