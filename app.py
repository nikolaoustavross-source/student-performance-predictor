"""
============================================================
  Student Performance Predictor — Flask App
  ----------------------------------------------------------
  Web app για πρόβλεψη επίδοσης φοιτητή (Pass/Fail).
  Χρησιμοποιεί προ-εκπαιδευμένο Logistic Regression model
  αποθηκευμένο ως student_model.pkl.

  Endpoints:
    GET  /         → επιστρέφει τη φόρμα (index.html)
    POST /predict  → δέχεται JSON, επιστρέφει JSON με πρόβλεψη
============================================================
"""

# ─────────────────────────────────────────────────────────────
#  Imports
# ─────────────────────────────────────────────────────────────
from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
from pathlib import Path


# ─────────────────────────────────────────────────────────────
#  1. Δημιουργία Flask εφαρμογής
# ─────────────────────────────────────────────────────────────
app = Flask(__name__)


# ─────────────────────────────────────────────────────────────
#  2. Φόρτωση του εκπαιδευμένου μοντέλου (μία φορά στο startup)
#
#  Το try/except εξασφαλίζει ότι ο server θα ξεκινήσει ακόμα
#  και αν λείπει το model.pkl — απλώς τα predicts θα επιστρέφουν
#  503 error. Χρήσιμο για debugging.
# ─────────────────────────────────────────────────────────────
MODEL_PATH = Path(__file__).parent / 'student_model.pkl'

try:
    model = joblib.load(MODEL_PATH)
    print(f"✓ Model loaded from {MODEL_PATH.name}")
    print(f"  Classes: {list(model.classes_)}")
except FileNotFoundError:
    print(f"⚠ Warning: {MODEL_PATH.name} not found — predictions will fail")
    model = None


# ─────────────────────────────────────────────────────────────
#  3. Home route — επιστρέφει τη φόρμα HTML
# ─────────────────────────────────────────────────────────────
@app.route('/')
def home():
    return render_template('index.html')


# ─────────────────────────────────────────────────────────────
#  4. Predict route — JSON API
#
#  Δέχεται POST request με JSON body, καλεί το model,
#  και επιστρέφει JSON με την πρόβλεψη.
# ─────────────────────────────────────────────────────────────
@app.route('/predict', methods=['POST'])
def predict():
    # ─── Έλεγχος ότι το model είναι φορτωμένο ───
    if model is None:
        return jsonify({"error": "Model not loaded"}), 503

    # ─── Έλεγχος ότι το request είναι JSON ───
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Request must be JSON"}), 400

    # ─── Validation: όλα τα απαιτούμενα πεδία υπάρχουν ───
    required_fields = [
        "study_hours", "attendance", "previous_grade",
        "assignments_submitted", "participation"
    ]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    try:
        # ─── Δημιουργία DataFrame στη μορφή που περιμένει το model ───
        # ΠΡΟΣΟΧΗ: τα ονόματα των στηλών πρέπει να ταιριάζουν ακριβώς
        # με αυτά που είδε το model κατά το training.
        # Στο notebook, το feature ονομάζεται "submitted_assignments"
        # — γι' αυτό κάνουμε rename εδώ από "assignments_submitted".
        new_student = pd.DataFrame({
            "study_hours":           [float(data['study_hours'])],
            "attendance":            [float(data['attendance'])],
            "previous_grade":        [float(data['previous_grade'])],
            "submitted_assignments": [int(data['assignments_submitted'])],
            # Καθαρίζουμε whitespace και κεφαλαιοποιούμε το πρώτο γράμμα
            # ώστε "medium", " Medium ", "MEDIUM" να γίνουν όλα "Medium"
            "participation":         [data['participation'].strip().capitalize()]
        })

        # ─── Πρόβλεψη ───
        prediction = model.predict(new_student)[0]

        # ─── Probability — παίρνουμε τη μέγιστη πιθανότητα ───
        # Αυτό δουλεύει ανεξάρτητα από το αν οι classes είναι
        # [0,1] ή ['Fail','Pass'] — πάντα δίνει το confidence
        # για την πρόβλεψη που έγινε.
        probability = model.predict_proba(new_student)[0].max()

        # ─── Κανονικοποίηση label ───
        # Το model μπορεί να επιστρέφει 1, "Pass", True ως positive class
        label = "Pass" if prediction in [1, "Pass", True] else "Fail"

        # ─── Επιστροφή response ως JSON ───
        return jsonify({
            "prediction":  label,
            "probability": round(float(probability) * 100, 2)   # ως ποσοστό
        })

    except (ValueError, TypeError) as e:
        # Λάθος τύπος δεδομένων (π.χ. string σε αριθμητικό πεδίο)
        return jsonify({"error": f"Invalid input: {e}"}), 400
    except Exception as e:
        # Οτιδήποτε άλλο πάει στραβά
        return jsonify({"error": str(e)}), 500


# ─────────────────────────────────────────────────────────────
#  5. Εκκίνηση του server
# ─────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("  Student Performance Predictor")
    print("  → http://localhost:5000")
    print("=" * 50 + "\n")
    app.run(debug=True, port=5000)
