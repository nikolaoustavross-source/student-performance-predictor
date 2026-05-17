# 📡 Customer Churn Predictor

A machine learning web application that predicts whether a telecom customer is likely to churn, built for **AIN5301EN – Introduction to AI, Assessment 2**.

> Dataset: [Telco Customer Churn – Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)

---

## 📁 Repository Structure

```
customer-churn-predictor/
├── churn_predictor.py        ← Full ML pipeline (Tasks 2–5)
├── app.py                    ← Flask web application MVP
├── templates/
│   └── index.html            ← Web form front-end
├── schema.sql                ← SQLite database schema
├── requirements.txt          ← Python dependencies
└── README.md                 ← This file
```

---

## ⚙️ Prerequisites

- **Python 3.10 or newer** — [download from python.org](https://www.python.org/downloads/)
- **pip** (comes with Python)
- A browser (Chrome, Firefox, Safari, Edge)

Check your Python version:
```bash
python3 --version
```

---

## 🚀 Setup — Step by Step

### Step 1 — Get the dataset

1. Go to [kaggle.com/datasets/blastchar/telco-customer-churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
2. Download `WA_Fn-UseC_-Telco-Customer-Churn.csv`
3. Place it in the same folder as `churn_predictor.py`

### Step 2 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Train the model

This runs the full ML pipeline and saves `churn_model.pkl`:

```bash
python3 churn_predictor.py
```

You will see accuracy scores, a classification report, and a saved chart (`churn_results.png`).

### Step 4 — Start the web app

```bash
python3 app.py
```

### Step 5 — Open in your browser

Go to: **http://localhost:5000**

Fill in the customer details and click **Predict Churn**.

---

## 🧪 Test Scenarios

| Scenario | Tenure | Contract | Monthly $ | Internet | Expected |
|---|---|---|---|---|---|
| High-risk customer | 1 month | Month-to-month | $85 | Fiber optic | **Churn ⚠️** |
| Loyal customer | 48 months | Two year | $55 | DSL | **No Churn ✅** |
| Borderline | 12 months | One year | $65 | DSL | **~50%** |

---

## 🛑 Stopping the App

Press **Ctrl + C** in the terminal.

## 🔄 Restarting Later

```bash
python3 app.py
```

No need to retrain — `churn_model.pkl` is already saved.

---

## 🗺 Architecture

```
┌─────────┐   POST JSON   ┌──────────┐   predict()   ┌─────────────────┐
│ Browser │ ────────────► │  Flask   │ ────────────► │ Random Forest   │
│  Form   │               │ (app.py) │               │ (churn_model.pkl│
└─────────┘ ◄──────────── └──────────┘ ◄──────────── └─────────────────┘
             JSON result
```

- **Frontend** (`templates/index.html`) — HTML form with all 19 Telco customer features, vanilla JS using `fetch()`
- **Backend** (`app.py`) — Flask with two routes: `/` serves the form, `/predict` runs inference
- **Model** (`churn_model.pkl`) — scikit-learn Random Forest trained on 7,043 customer records

---

## 📊 Model Performance

| Model | Accuracy | ROC-AUC |
|---|---|---|
| Logistic Regression | ~80% | ~0.84 |
| Random Forest | ~79% | ~0.82 |

Random Forest is used in the web app. Results are generated when you run `churn_predictor.py`.

---

## 🐛 Troubleshooting

**`python3: command not found`**
Try `python` instead of `python3`.

**`ModuleNotFoundError`**
Run `pip install -r requirements.txt` again.

**`churn_model.pkl not found`**
You need to run `churn_predictor.py` before `app.py`.

**`Address already in use` (port 5000)**
Another app is using port 5000. Change the port in `app.py`:
```python
app.run(debug=True, port=5001)
```
Then go to `http://localhost:5001`.

**`FileNotFoundError: WA_Fn-UseC_-Telco-Customer-Churn.csv`**
Make sure the CSV file is in the same folder as `churn_predictor.py`.

---

## ⚠️ Limitations

- Model trained on a single static dataset — not updated in real time
- No user authentication
- Predictions are not stored (no active database connection in MVP)
- For proof-of-concept only — not production-ready

---

## 📚 Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Web Framework | Flask 3.0 |
| ML Library | scikit-learn 1.6.1 |
| Data | pandas, numpy |
| Visualisation | matplotlib, seaborn |
| Model Storage | joblib |
| Frontend | HTML, CSS, Vanilla JavaScript |
| Database Schema | SQLite |
