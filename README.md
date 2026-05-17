# Student Performance Predictor — MVP

A web app that predicts whether a student will **Pass or Fail** a course using Machine Learning (Logistic Regression).

> **Example project** for AI Assessment 002 (Portfolio).

---

# 📁 Project Structure

```
student-performance-mvp/
├── README.md                       ← This file
├── requirements.txt                ← Dependencies (pinned versions)
├── app.py                          ← Flask backend
├── student_model.pkl               ← Trained ML model
├── project_model_example.ipynb     ← Training notebook
└── templates/
    └── index.html                  ← Frontend (HTML + CSS + JS)
```

---

# ⚙️ Prerequisites

- **Python 3.10 or newer** ([download from python.org](https://www.python.org/downloads/))
- **pip** (comes bundled with Python)
- A browser (Chrome, Firefox, Edge, Safari)

To check if Python is installed:

```bash
python --version
# e.g. Python 3.11.5
```

On Mac/Linux you may need to use `python3` instead of `python`.

---

# 🚀 Installation — Step by Step

# Step 1 — Open a terminal inside the project folder

Download / unzip the project and open a terminal **inside** the `student-performance-mvp/` folder.

```bash
cd path/to/student-performance-mvp
```

# Step 2 — Create a virtual environment

A virtual environment (venv) is an isolated Python space just for this project.
This way, the packages we install don't affect other projects on your computer.

```bash
python -m venv venv
```

This creates a `venv/` folder inside the project.

# Step 3 — Activate the venv

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

**Mac / Linux:**
```bash
source venv/bin/activate
```

When active, you will see `(venv)` at the start of your command line.

# Step 4 — Install dependencies

```bash
pip install -r requirements.txt
```

This will install Flask, scikit-learn, pandas, etc. (~50 MB).

# Step 5 — Start the application

```bash
python app.py
```

You should see output like:
```
✓ Model loaded from student_model.pkl
  Classes: ['Fail', 'Pass']

==================================================
  Student Performance Predictor
  → http://localhost:5000
==================================================

 * Running on http://127.0.0.1:5000
```

# Step 6 — Open in your browser

Go to: **http://localhost:5000**

Fill in the form and click **Predict**.

---

# 🛑 How to stop the app

In the terminal, press **Ctrl + C**.

# 🔄 How to start it again later

From the project folder:

```bash
# 1. Activate venv
source venv/bin/activate          # Mac/Linux
venv\Scripts\activate             # Windows

# 2. Start the app
python app.py
```

---

# 🧪 Test Scenarios

| Scenario | Study | Attend | Grade | Assignments | Participation | Expected |
|---|---|---|---|---|---|---|
| Strong student | 10 | 95 | 85 | 5 | High | **Pass** (high confidence) |
| At-risk student | 2 | 40 | 30 | 1 | Low | **Fail** (high confidence) |
| Borderline | 5 | 65 | 55 | 2 | Medium | **~50%** confidence |

---

# 📓 How to retrain the model

If you want to change the data or the algorithm:

```bash
# With venv active:
jupyter notebook
```

Open `project_model_example.ipynb` and run all cells.
The new model will be saved as `student_model.pkl` (replaces the old one).

Restart `python app.py` to load the new model.

---

# 🐛 Troubleshooting

# `python: command not found`
Try `python3` instead of `python`.

# `pip: command not found`
Install pip: `python -m ensurepip --upgrade`

# `Address already in use` (port 5000)
Another application is running on port 5000.
- Stop it, or
- Change the port in `app.py`: `app.run(debug=True, port=5001)`

# `InconsistentVersionWarning` or `ModuleNotFoundError` when loading the model
Wrong version of scikit-learn. Make sure your venv is active and run:
```bash
pip install -r requirements.txt --force-reinstall
```

# The page shows "Internal Server Error"
Check the terminal — the full error message is displayed there.

# venv activation doesn't work in PowerShell
Run as administrator:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

# 🗺 Architecture

```
┌─────────┐    POST     ┌──────────┐    predict()    ┌──────────┐
│ Browser │ ────JSON──► │  Flask   │ ──────────────► │  Model   │
│ (form)  │             │ (app.py) │                 │  (.pkl)  │
└─────────┘ ◄──JSON──── └──────────┘ ◄───── label ── └──────────┘
```

**Frontend (templates/index.html)**: HTML form + CSS + vanilla JS using `fetch()`

**Backend (app.py)**: Flask with 2 routes — `/` for the form, `/predict` for inference

**Model (student_model.pkl)**: scikit-learn Pipeline containing a preprocessor (StandardScaler + OneHotEncoder) + LogisticRegression

---

# ⚠️ Limitations

- Trained on **only 10 samples** — proof of concept, not production-ready
- No authentication or user management
- No database — every prediction is lost after the session ends
- Single-page app — no prediction history

See the reflection document in your portfolio for an analysis of limitations and possible improvements (Task 5).

---

# 📚 Tech Stack

- **Python 3.10+**
- **Flask 3.0** — micro web framework
- **scikit-learn 1.6.1** — ML library
- **pandas / numpy** — data manipulation
- **joblib** — model serialization
- **Vanilla JavaScript** — no frontend frameworks
