import pandas as pd
import numpy as np
import os

def enrich_kaggle_data(input_csv, output_csv):
    """Reads Kaggle base data and simulates ticket logs based on churn status."""
    print("Reading Kaggle dataset...")
    try:
        df = pd.read_csv(input_csv)
    except FileNotFoundError:
        print(f"Error: Could not find {input_csv}. Please ensure it is saved in the data folder.")
        return

    num_records = len(df)
    np.random.seed(42)
    
    # Helper function: Generates higher/lower numbers based on if they churned
    def generate_based_on_churn(churn_series, true_mean, false_mean):
        return np.where(
            churn_series == 'Yes', 
            np.random.poisson(true_mean, num_records), 
            np.random.poisson(false_mean, num_records)
        )

    print("Simulating ticket logs...")
    # 1. Ticket frequency (7d, 30d, 90d) - Churned users have more tickets
    df['tickets_7d'] = generate_based_on_churn(df['Churn'], true_mean=3, false_mean=0)
    df['tickets_30d'] = generate_based_on_churn(df['Churn'], true_mean=8, false_mean=1)
    df['tickets_90d'] = generate_based_on_churn(df['Churn'], true_mean=15, false_mean=3)
    
    # 2. Ticket sentiment score (0.0 to 1.0) - Churned users are angrier (lower score)
    df['ticket_sentiment_score'] = np.where(
        df['Churn'] == 'Yes',
        np.random.uniform(0.1, 0.4, num_records),
        np.random.uniform(0.5, 0.9, num_records)
    )
    
    # 3. Ticket category counts
    df['ticket_category_billing'] = generate_based_on_churn(df['Churn'], 4, 1)
    df['ticket_category_tech'] = generate_based_on_churn(df['Churn'], 5, 1)
    
    # 4. Time between tickets
    df['time_between_tickets_days'] = np.where(
        df['Churn'] == 'Yes',
        np.random.exponential(5, num_records).round(1),  # Frequent tickets
        np.random.exponential(25, num_records).round(1)  # Infrequent tickets
    )
    
    # 5. Change in monthly charges
    df['change_in_monthly_charges'] = np.random.normal(5, 10, num_records).round(2)
    
    # Save the enriched dataset
    df.to_csv(output_csv, index=False)
    print(f"✅ Enriched data successfully saved to {output_csv}")

if __name__ == "__main__":
    enrich_kaggle_data("data/raw_telco_data.csv", "data/processed_telco_data.csv")