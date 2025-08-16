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

# Web pages
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/screenAu")
def screen_au_page():
    return render_template("screenAu.html")

@app.route("/SignIn")
def sign_in_page():
    return render_template("!SignIn.html")

@app.route("/Chat")
def chat_page():
    return render_template("chat.html")

@app.route("/eform")
def eform_page():
    return render_template("eform.html")

@app.route("/form")
def form_page():
    return render_template("form.html")

@app.route("/history")
def history_page():
    return render_template("history.html")

@app.route("/home")
def home_page():
    return render_template("home.html")

@app.route("/info-th")
def info_th_page():
    return render_template("info-th.html")

@app.route("/info")
def info_page():
    return render_template("info.html")

@app.route("/r0")
def r0_page():
    return render_template("r0.html")

@app.route("/r1")
def r1_page():
    return render_template("r1.html")

@app.route("/r2")
def r2_page():
    return render_template("r2.html")

@app.route("/spec")
def spec_page():
    return render_template("spec.html")

@app.route("/tele")
def tele_page():
    return render_template("tele.html")

@app.route("/tele2")
def tele2_page():
    return render_template("tele2.html")

@app.route("/tele3")
def tele3_page():
    return render_template("tele3.html")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5050))
    app.run(debug=False, host="0.0.0.0", port=port)