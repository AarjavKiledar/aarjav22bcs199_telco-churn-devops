from app.models import CustomerData

def evaluate_churn_risk(data: CustomerData) -> tuple[str, str]:
    # Rule 1: If customer has >5 tickets in last 30 days -> HIGH RISK
    if data.tickets_last_30_days > 5:
        return "High", "Rule 1: >5 tickets in last 30 days"
    
    # Rule 3: If contract type = Month-to-Month + complaint ticket -> HIGH RISK
    # (Evaluated before Medium risk to ensure High risk takes precedence)
    if data.contract_type == "Month-to-Month" and data.has_complaint_ticket:
        return "High", "Rule 3: Month-to-Month contract + complaint ticket"
    
    # Rule 2: If monthly charges increased + 3 tickets raised -> MEDIUM RISK
    if data.monthly_charges_increased and data.recent_tickets_raised >= 3:
        return "Medium", "Rule 2: Monthly charges increased + >=3 tickets raised"
    
    # Default fallback if no rules are triggered
    return "Low", "No high/medium risk rules triggered"