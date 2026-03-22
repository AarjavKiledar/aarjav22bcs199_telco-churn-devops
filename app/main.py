from fastapi import FastAPI
import logging
from app.models import CustomerData, ChurnRiskResponse
from app.rules import evaluate_churn_risk

# Setup basic logging to print to the terminal
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Telco Churn Risk API (Rule-Based Engine)")

@app.post("/predict-risk", response_model=ChurnRiskResponse)
def predict_risk(customer: CustomerData):
    # Pass data to the rule engine
    risk, rule_triggered = evaluate_churn_risk(customer)
    
    # Log the output (Crucial for your assignment screenshots)
    logger.info(f"Customer {customer.customer_id} evaluated as {risk.upper()} RISK. Triggered by: {rule_triggered}")
    
    return ChurnRiskResponse(
        customer_id=customer.customer_id,
        risk_category=risk,
        triggered_rule=rule_triggered
    )