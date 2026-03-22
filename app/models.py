from pydantic import BaseModel

class CustomerData(BaseModel):
    customer_id: str
    tenure: int
    MonthlyCharges: float
    tickets_7d: int
    tickets_30d: int
    tickets_90d: int
    ticket_sentiment_score: float
    ticket_category_billing: int
    ticket_category_tech: int
    time_between_tickets_days: float
    change_in_monthly_charges: float

class ChurnRiskResponse(BaseModel):
    customer_id: str
    churn_prediction: int        # 1 for Yes, 0 for No
    churn_probability: float     # Percentage certainty
    risk_category: str           # Low/Medium/High mapped from probability
    system_used: str             # To prove we are using ML now