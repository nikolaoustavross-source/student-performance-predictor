# Customer Churn Predictor
## AIN5301EN – Introduction to AI | Assessment 2
### Student ID: 2426525

A Customer Churn Predictor web app built with Flask and Machine Learning (Logistic Regression + Random Forest).

---

## How to Run

### 1. Clone the repo
```bash
git clone https://github.com/nikolaoustavross-source/student-performance-predictor.git
cd student-performance-predictor
```

### 2. Install dependencies
```bash
pip3 install flask joblib scikit-learn pandas numpy matplotlib seaborn scipy
```

### 3. Train the model
```bash
python3 churn_predictor.py
```

### 4. Start the web app
```bash
python3 app.py
```

### 5. Open the app
👉 Click or paste this in your browser: **http://localhost:5001**

---

## Project Structure
| File | Description |
|------|-------------|
| `app.py` | Flask web application |
| `churn_predictor.py` | ML model training script |
| `churn_model.pkl` | Trained Random Forest model |
| `churn_results.png` | Model evaluation charts |
| `WA_Fn-UseC_-Telco-Customer-Churn.csv` | Telco Customer Churn dataset |
| `templates/` | HTML templates for the web app |
| `schema.sql` | Database schema |

---

## AI Technique
- **Classification** using Logistic Regression and Random Forest
- Dataset: [Telco Customer Churn – Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
- Accuracy: ~80% | ROC-AUC: ~0.84

---

## Note
The app runs locally. After running `python3 app.py`, open **http://localhost:5001** in your browser.
