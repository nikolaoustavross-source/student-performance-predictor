"""
============================================================
  Student Performance Predictor — Flask App
  ----------------------------------------------------------
  Web app to predict student performance (Pass/Fail).
  Uses a pre-trained Logistic Regression model
  stored as student_model.pkl.

  Endpoints:
    GET  /         → returns the form (index.html)
    POST /predict  → accepts JSON, returns JSON with prediction
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
#  1. Create Flask application
# ─────────────────────────────────────────────────────────────
app = Flask(__name__)


# ─────────────────────────────────────────────────────────────
#  2. Load the trained model (once at startup)
#
#  The try/except ensures the server will start even if
#  model.pkl is missing — predictions will simply return
#  a 503 error. Useful for debugging.
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
#  3. Home route — returns the HTML form
# ─────────────────────────────────────────────────────────────
@app.route('/')
def home():
    return render_template('index.html')


# ─────────────────────────────────────────────────────────────
#  4. Predict route — JSON API
#
#  Accepts a POST request with a JSON body, calls the model,
#  and returns JSON with the prediction result.
# ─────────────────────────────────────────────────────────────
@app.route('/predict', methods=['POST'])
def predict():
    # ─── Check that the model is loaded ───
    if model is None:
        return jsonify({"error": "Model not loaded"}), 503

    # ─── Check that the request body is JSON ───
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Request must be JSON"}), 400

    # ─── Validation: all required fields must be present ───
    required_fields = [
        "study_hours", "attendance", "previous_grade",
        "assignments_submitted", "participation"
    ]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    try:
        # ─── Build DataFrame in the format the model expects ───
        # NOTE: column names must match exactly what the model
        # saw during training. In the notebook, the feature is
        # called "submitted_assignments", so we rename it here
        # from "assignments_submitted".
        new_student = pd.DataFrame({
            "study_hours":           [float(data['study_hours'])],
            "attendance":            [float(data['attendance'])],
            "previous_grade":        [float(data['previous_grade'])],
            "submitted_assignments": [int(data['assignments_submitted'])],
            # Strip whitespace and capitalise first letter so
            # "medium", " Medium ", "MEDIUM" all become "Medium"
            "participation":         [data['participation'].strip().capitalize()]
        })

        # ─── Make prediction ───
        prediction = model.predict(new_student)[0]

        # ─── Probability — take the highest probability class ───
        # This works regardless of whether classes are
        # [0,1] or ['Fail','Pass'] — always gives the confidence
        # for the predicted class.
        probability = model.predict_proba(new_student)[0].max()

        # ─── Normalise the label ───
        # The model may return 1, "Pass", or True as the positive class
        label = "Pass" if prediction in [1, "Pass", True] else "Fail"

        # ─── Return response as JSON ───
        return jsonify({
            "prediction":  label,
            "probability": round(float(probability) * 100, 2)   # as percentage
        })

    except (ValueError, TypeError) as e:
        # Wrong data type (e.g. string in a numeric field)
        return jsonify({"error": f"Invalid input: {e}"}), 400
    except Exception as e:
        # Anything else that goes wrong
        return jsonify({"error": str(e)}), 500


# ─────────────────────────────────────────────────────────────
#  5. Start the server
# ─────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("  Student Performance Predictor")
    print("  → http://localhost:5000")
    print("=" * 50 + "\n")
    app.run(debug=True, port=5000)
