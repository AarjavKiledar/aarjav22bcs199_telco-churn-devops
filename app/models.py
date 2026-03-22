from pydantic import BaseModel

class CustomerData(BaseModel):
    customer_id: str
    monthly_charges_increased: bool
    contract_type: str  # e.g., "Month-to-Month", "One year"
    tickets_last_30_days: int
    recent_tickets_raised: int
    has_complaint_ticket: bool

class ChurnRiskResponse(BaseModel):
    customer_id: str
    risk_category: str
    triggered_rule: str