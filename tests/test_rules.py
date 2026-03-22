from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_rule_1_high_risk():
    """Test: >5 tickets in last 30 days -> HIGH RISK"""
    payload = {
        "customer_id": "TEST-001",
        "monthly_charges_increased": False,
        "contract_type": "Two year",
        "tickets_last_30_days": 6,  # Triggers Rule 1
        "recent_tickets_raised": 0,
        "has_complaint_ticket": False
    }
    response = client.post("/predict-risk", json=payload)
    assert response.status_code == 200
    assert response.json()["risk_category"] == "High"
    assert "Rule 1" in response.json()["triggered_rule"]

def test_rule_3_high_risk():
    """Test: Month-to-Month + complaint ticket -> HIGH RISK"""
    payload = {
        "customer_id": "TEST-002",
        "monthly_charges_increased": False,
        "contract_type": "Month-to-Month", # Triggers Rule 3
        "tickets_last_30_days": 1,
        "recent_tickets_raised": 0,
        "has_complaint_ticket": True       # Triggers Rule 3
    }
    response = client.post("/predict-risk", json=payload)
    assert response.status_code == 200
    assert response.json()["risk_category"] == "High"
    assert "Rule 3" in response.json()["triggered_rule"]

def test_rule_2_medium_risk():
    """Test: monthly charges increased + >=3 tickets raised -> MEDIUM RISK"""
    payload = {
        "customer_id": "TEST-003",
        "monthly_charges_increased": True, # Triggers Rule 2
        "contract_type": "One year",
        "tickets_last_30_days": 2,
        "recent_tickets_raised": 3,        # Triggers Rule 2
        "has_complaint_ticket": False
    }
    response = client.post("/predict-risk", json=payload)
    assert response.status_code == 200
    assert response.json()["risk_category"] == "Medium"
    assert "Rule 2" in response.json()["triggered_rule"]

def test_low_risk():
    """Test: No rules triggered -> LOW RISK"""
    payload = {
        "customer_id": "TEST-004",
        "monthly_charges_increased": False,
        "contract_type": "Two year",
        "tickets_last_30_days": 1,
        "recent_tickets_raised": 1,
        "has_complaint_ticket": False
    }
    response = client.post("/predict-risk", json=payload)
    assert response.status_code == 200
    assert response.json()["risk_category"] == "Low"