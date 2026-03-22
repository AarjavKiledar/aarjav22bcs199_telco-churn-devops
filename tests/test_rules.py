from fastapi.testclient import TestClient
from app.main import app

def test_ml_prediction_endpoint():
    """Test that the ML endpoint accepts the new feature schema and returns a probability."""
    # Wrapping in 'with TestClient' forces the startup/lifespan events to run
    with TestClient(app) as client:
        payload = {
            "customer_id": "TEST-ML-001",
            "tenure": 2,
            "MonthlyCharges": 85.0,
            "tickets_7d": 4,
            "tickets_30d": 12,
            "tickets_90d": 25,
            "ticket_sentiment_score": 0.2,
            "ticket_category_billing": 5,
            "ticket_category_tech": 8,
            "time_between_tickets_days": 2.5,
            "change_in_monthly_charges": 15.0
        }
        
        response = client.post("/predict-risk", json=payload)
        
        # Check that the API successfully processed the request
        assert response.status_code == 200
        
        data = response.json()
        
        # Verify it's using the ML model and returning the expected data types
        assert data["customer_id"] == "TEST-ML-001"
        assert "churn_probability" in data
        assert type(data["churn_probability"]) == float
        assert data["system_used"] == "Random Forest ML Model"

def test_missing_features_returns_422():
    """Test that missing required ML features throws a validation error."""
    with TestClient(app) as client:
        payload = {
            "customer_id": "TEST-ML-002",
            "tenure": 5
            # Missing all other required features
        }
        
        response = client.post("/predict-risk", json=payload)
        assert response.status_code == 422 # FastAPI standard validation error code