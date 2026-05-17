# ============================================================
# AIN5301EN – Introduction to AI
# Assessment 2 – Customer Churn Predictor
# Student ID: 2426525
# ============================================================

# ──────────────────────────────────────────────────────────
# TASK 2 & 3 – Dataset + AI Implementation
# Dataset: Telco Customer Churn (Kaggle)
# https://www.kaggle.com/datasets/blastchar/telco-customer-churn
# ──────────────────────────────────────────────────────────

# ── 1. IMPORTS ────────────────────────────────────────────
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report, confusion_matrix,
    accuracy_score, roc_auc_score, roc_curve
)
import warnings
warnings.filterwarnings('ignore')

print("✅ All libraries imported successfully")

# ── 2. LOAD DATASET ───────────────────────────────────────
# Download from Kaggle: WA_Fn-UseC_-Telco-Customer-Churn.csv
# Place in the same folder as this script
df = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")
print(f"\n📊 Dataset shape: {df.shape}")
print(df.head())

# ── 3. EXPLORATION ────────────────────────────────────────
print("\n📌 Column info:")
print(df.dtypes)
print("\n📌 Missing values:")
print(df.isnull().sum())
print("\n📌 Target distribution (Churn):")
print(df['Churn'].value_counts())
print(df['Churn'].value_counts(normalize=True).round(3))

# ── 4. PREPROCESSING ─────────────────────────────────────
# Fix TotalCharges (has spaces, should be numeric)
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df['TotalCharges'].fillna(df['TotalCharges'].median(), inplace=True)

# Drop customerID (not predictive)
df.drop('customerID', axis=1, inplace=True)

# Encode binary target
df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})

# Encode categorical features
# We save the label encoders so the Flask app can use the same encoding
cat_cols = df.select_dtypes(include='object').columns.tolist()
print(f"\n🔠 Categorical columns to encode: {cat_cols}")

encoders = {}
le = LabelEncoder()
for col in cat_cols:
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

print("\n✅ Preprocessing complete. Sample:")
print(df.head())

# ── 5. FEATURE / TARGET SPLIT ─────────────────────────────
X = df.drop('Churn', axis=1)
y = df['Churn']

# Save column order — Flask app must send features in this exact order
FEATURE_COLUMNS = list(X.columns)
print(f"\n📐 Features: {FEATURE_COLUMNS}")

# ── 6. TRAIN / TEST SPLIT ─────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"\n📊 Train size: {X_train.shape[0]} | Test size: {X_test.shape[0]}")

# Scale features (important for Logistic Regression)
scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc  = scaler.transform(X_test)

# ── 7. MODEL 1 – LOGISTIC REGRESSION ─────────────────────
lr = LogisticRegression(max_iter=1000, random_state=42)
lr.fit(X_train_sc, y_train)
y_pred_lr = lr.predict(X_test_sc)

print("\n=== Logistic Regression ===")
print(f"Accuracy : {accuracy_score(y_test, y_pred_lr):.4f}")
print(f"ROC-AUC  : {roc_auc_score(y_test, lr.predict_proba(X_test_sc)[:,1]):.4f}")
print(classification_report(y_test, y_pred_lr, target_names=['No Churn','Churn']))

# ── 8. MODEL 2 – RANDOM FOREST ───────────────────────────
rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)

print("\n=== Random Forest ===")
print(f"Accuracy : {accuracy_score(y_test, y_pred_rf):.4f}")
print(f"ROC-AUC  : {roc_auc_score(y_test, rf.predict_proba(X_test)[:,1]):.4f}")
print(classification_report(y_test, y_pred_rf, target_names=['No Churn','Churn']))

# ── 9. VISUALISATION ─────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# 9a – Confusion Matrix (Random Forest)
cm = confusion_matrix(y_test, y_pred_rf)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[0],
            xticklabels=['No Churn','Churn'],
            yticklabels=['No Churn','Churn'])
axes[0].set_title('Random Forest – Confusion Matrix')
axes[0].set_ylabel('Actual'); axes[0].set_xlabel('Predicted')

# 9b – Feature Importance
feat_imp = pd.Series(rf.feature_importances_, index=X.columns).nlargest(10)
feat_imp.sort_values().plot(kind='barh', ax=axes[1], color='steelblue')
axes[1].set_title('Top 10 Feature Importances')
axes[1].set_xlabel('Importance Score')

# 9c – ROC Curves
fpr_lr, tpr_lr, _ = roc_curve(y_test, lr.predict_proba(X_test_sc)[:,1])
fpr_rf, tpr_rf, _ = roc_curve(y_test, rf.predict_proba(X_test)[:,1])
axes[2].plot(fpr_lr, tpr_lr, label=f'LR  AUC={roc_auc_score(y_test, lr.predict_proba(X_test_sc)[:,1]):.3f}')
axes[2].plot(fpr_rf, tpr_rf, label=f'RF  AUC={roc_auc_score(y_test, rf.predict_proba(X_test)[:,1]):.3f}')
axes[2].plot([0,1],[0,1],'k--')
axes[2].set_title('ROC Curve Comparison')
axes[2].set_xlabel('False Positive Rate')
axes[2].set_ylabel('True Positive Rate')
axes[2].legend()

plt.tight_layout()
plt.savefig('churn_results.png', dpi=150)
plt.show()
print("\n✅ Chart saved as churn_results.png")

# ── 10. EXAMPLE PREDICTION ────────────────────────────────
# Simulate a new customer
sample = X_test.iloc[[0]].copy()
pred_class = rf.predict(sample)[0]
pred_prob  = rf.predict_proba(sample)[0][1]

print("\n🔮 Example Prediction:")
print(f"   Input features (first test row): {sample.values}")
print(f"   Predicted class : {'Churn ⚠️' if pred_class == 1 else 'No Churn ✅'}")
print(f"   Churn probability: {pred_prob:.2%}")

# ── 11. SAVE MODEL & SCALER FOR FLASK APP ─────────────────
# Save the Random Forest model, scaler, and feature column list
# so the Flask web app (app.py) can load and use them directly
joblib.dump({
    'model':    rf,
    'scaler':   scaler,
    'features': FEATURE_COLUMNS,
    'encoders': encoders
}, 'churn_model.pkl')

print("\n✅ Model saved as churn_model.pkl")
print("   Run 'python app.py' to start the web app.")
