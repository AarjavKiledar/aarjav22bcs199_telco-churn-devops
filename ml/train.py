import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, roc_auc_score, precision_score, recall_score
import joblib
import os

def train_model():
    data_path = "data/processed_telco_data.csv"
    if not os.path.exists(data_path):
        print("Data not found. Run simulate_data.py first.")
        return
        
    print("Loading enriched data...")
    df = pd.read_csv(data_path)
    
    # Convert Kaggle's text 'Yes'/'No' Churn to binary 1/0 for the ML model
    df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})
    
    # Combine original Kaggle features with our simulated features
    features = [
        "tenure", "MonthlyCharges",                   # Kaggle Base Features
        "tickets_7d", "tickets_30d", "tickets_90d",   # Simulated Features
        "ticket_sentiment_score", "ticket_category_billing", 
        "ticket_category_tech", "time_between_tickets_days", 
        "change_in_monthly_charges"
    ]
    
    X = df[features]
    y = df["Churn"]
    
    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    model.fit(X_train, y_train)
    
    # Predictions
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    
    # Evaluation Metrics
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_prob)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    
    print("\n--- Model Evaluation ---")
    print(f"F1 Score:         {f1:.4f}")
    print(f"ROC-AUC:          {roc_auc:.4f}")
    print(f"Precision:        {precision:.4f}")
    print(f"Recall:           {recall:.4f}")
    print("------------------------\n")
    
    # Save the model artifact
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/churn_model.pkl")
    # Also save the feature names so the API knows what to expect later
    joblib.dump(features, "models/model_features.pkl")
    print("✅ Model and features saved to models/ directory")

if __name__ == "__main__":
    train_model()