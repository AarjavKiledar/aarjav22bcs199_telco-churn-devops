from fastapi import FastAPI, HTTPException
import logging
import joblib
import pandas as pd
from app.models import CustomerData, ChurnRiskResponse
import os
from contextlib import asynccontextmanager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the ML model and features on startup
MODEL_PATH = "models/churn_model.pkl"
FEATURES_PATH = "models/model_features.pkl"

model = None
feature_names = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # This runs on startup
    global model, feature_names
    if os.path.exists(MODEL_PATH) and os.path.exists(FEATURES_PATH):
        model = joblib.load(MODEL_PATH)
        feature_names = joblib.load(FEATURES_PATH)
        logger.info("✅ ML Model and features loaded successfully.")
    else:
        logger.warning("⚠️ Model artifacts not found. API will fail on prediction.")
    yield
    # Anything after yield runs on shutdown (we don't need anything right now)

app = FastAPI(title="Telco Churn Risk API (ML Inference)", lifespan=lifespan)

@app.post("/predict-risk", response_model=ChurnRiskResponse)
def predict_risk(customer: CustomerData):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded.")

    # Convert incoming JSON payload to a dictionary
    customer_dict = customer.dict()
    
    # Extract only the features the model expects, in the exact order
    try:
        input_data = [customer_dict[feature] for feature in feature_names]
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing feature: {e}")

    # Convert to a 2D array/DataFrame for Scikit-Learn
    input_df = pd.DataFrame([input_data], columns=feature_names)

    # Make the prediction
    prediction = int(model.predict(input_df)[0])
    probability = float(model.predict_proba(input_df)[0][1])

    # Map probability to risk category for the business
    if probability > 0.7:
        risk = "High"
    elif probability > 0.4:
        risk = "Medium"
    else:
        risk = "Low"

    logger.info(f"Customer {customer.customer_id} | ML Prediction: {prediction} | Prob: {probability:.2f} | Risk: {risk}")

    return ChurnRiskResponse(
        customer_id=customer.customer_id,
        churn_prediction=prediction,
        churn_probability=round(probability, 4),
        risk_category=risk,
        system_used="Random Forest ML Model"
    )