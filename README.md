## 🧠 Architecture & Theory Explanation

### 1. What broke when ML was added?
When Machine Learning was introduced, the system stopped being **purely deterministic**. 
* **In the DevOps stage:** Fixed rules guaranteed that the same input would always produce the exact same output. 
* **With ML:** The output is now probabilistic and heavily dependent on the training data distribution. 

This makes reproducibility fragile and shifts the debugging focus away from syntax errors and toward data quality issues. It also introduces entirely new failure modes, such as silent performance degradation, data drift, and training-serving skew (feature mismatch).

### 2. Why DevOps alone is insufficient?
Traditional DevOps is built on the assumption that **code defines system behavior** and that unit tests can fully validate that correctness. ML systems violate this assumption because **data drives behavior more than the code itself**. 

While DevOps tools are great at managing infrastructure and API lifecycles, they cannot unit-test a model's statistical accuracy. Without MLOps, a deployed model will naturally decay over time as real-world data changes, and DevOps alone provides no visibility into this degradation. MLOps is required to add data lineage, experiment tracking, and continuous evaluation loops.

### 3. What new risks ML introduces?
Adding ML introduces three distinct categories of risk:
* **📊 Data Risks:** The system is now vulnerable to training data bias, label noise, and distribution shifts over time.
* **⚙️ Operational Risks:** The system can suffer from model drift (degrading performance without triggering standard IT alerts), non-reproducible training environments, and mismatches between how features are engineered in training versus production.
* **💼 Business Risks:** Probabilistic systems can generate false positives (e.g., predicting a loyal customer will churn), or suffer from overfitting, leading to unstable and unreliable business decisions. Unlike traditional software where failures are obvious and binary, ML failures are often gradual and invisible until business metrics collapse.
