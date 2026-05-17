-- ============================================================
--  AIN5301EN – Introduction to AI
--  Assessment 2 – Customer Churn Predictor
--  Database Schema (SQLite)
-- ============================================================
--  Stores prediction history from the Flask web app.
--
--  To initialise the database, run once:
--    sqlite3 churn.db < schema.sql
--
--  Or via Python:
--    import sqlite3
--    conn = sqlite3.connect('churn.db')
--    conn.executescript(open('schema.sql').read())
-- ============================================================

-- Drop tables if they already exist (clean reset)
DROP TABLE IF EXISTS predictions;
DROP TABLE IF EXISTS feedback;

-- ──────────────────────────────────────────────────────────
--  TABLE: predictions
--  Stores every prediction made via the /predict endpoint.
--  Columns mirror the input fields in templates/index.html.
-- ──────────────────────────────────────────────────────────
CREATE TABLE predictions (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Customer demographics
    gender             TEXT    NOT NULL CHECK(gender IN ('Male', 'Female')),
    senior_citizen     INTEGER NOT NULL CHECK(senior_citizen IN (0, 1)),
    partner            TEXT    NOT NULL CHECK(partner IN ('Yes', 'No')),
    dependents         TEXT    NOT NULL CHECK(dependents IN ('Yes', 'No')),

    -- Account info
    tenure             INTEGER NOT NULL,             -- months with company
    contract           TEXT    NOT NULL,             -- Month-to-month / One year / Two year
    paperless_billing  TEXT    NOT NULL CHECK(paperless_billing IN ('Yes', 'No')),
    payment_method     TEXT    NOT NULL,
    monthly_charges    REAL    NOT NULL,             -- $ per month
    total_charges      REAL    NOT NULL,             -- $ total spent

    -- Phone services
    phone_service      TEXT    NOT NULL CHECK(phone_service IN ('Yes', 'No')),
    multiple_lines     TEXT    NOT NULL,

    -- Internet services
    internet_service   TEXT    NOT NULL,             -- DSL / Fiber optic / No
    online_security    TEXT    NOT NULL,
    online_backup      TEXT    NOT NULL,
    device_protection  TEXT    NOT NULL,
    tech_support       TEXT    NOT NULL,
    streaming_tv       TEXT    NOT NULL,
    streaming_movies   TEXT    NOT NULL,

    -- Model output
    prediction         TEXT    NOT NULL CHECK(prediction IN ('Churn', 'No Churn')),
    probability        REAL    NOT NULL,             -- 0.00–100.00 % churn probability

    -- Metadata
    created_at         DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ──────────────────────────────────────────────────────────
--  TABLE: feedback
--  Optional — lets users record whether the prediction
--  was actually correct (useful for model improvement).
-- ──────────────────────────────────────────────────────────
CREATE TABLE feedback (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    prediction_id  INTEGER NOT NULL
                   REFERENCES predictions(id) ON DELETE CASCADE,
    actual_outcome TEXT    NOT NULL CHECK(actual_outcome IN ('Churn', 'No Churn')),
    notes          TEXT,                             -- free-text comment
    created_at     DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ──────────────────────────────────────────────────────────
--  INDEXES — speed up common queries
-- ──────────────────────────────────────────────────────────

-- Filter predictions by churn outcome
CREATE INDEX idx_predictions_prediction ON predictions(prediction);

-- Filter predictions by date (e.g. recent history)
CREATE INDEX idx_predictions_created_at ON predictions(created_at);

-- Filter predictions by contract type (common business query)
CREATE INDEX idx_predictions_contract ON predictions(contract);

-- Look up feedback by prediction
CREATE INDEX idx_feedback_prediction_id ON feedback(prediction_id);

-- ──────────────────────────────────────────────────────────
--  SAMPLE DATA — useful for testing
-- ──────────────────────────────────────────────────────────
INSERT INTO predictions (
    gender, senior_citizen, partner, dependents, tenure,
    contract, paperless_billing, payment_method, monthly_charges, total_charges,
    phone_service, multiple_lines, internet_service, online_security, online_backup,
    device_protection, tech_support, streaming_tv, streaming_movies,
    prediction, probability
) VALUES
    -- High-risk customer (month-to-month, fiber optic, short tenure)
    ('Male',   0, 'No',  'No',  2,
     'Month-to-month', 'Yes', 'Electronic check', 85.50, 171.00,
     'Yes', 'No', 'Fiber optic', 'No', 'No',
     'No', 'No', 'Yes', 'Yes',
     'Churn', 87.40),

    -- Loyal customer (two year contract, long tenure)
    ('Female', 0, 'Yes', 'Yes', 52,
     'Two year', 'No', 'Bank transfer (automatic)', 55.00, 2860.00,
     'Yes', 'Yes', 'DSL', 'Yes', 'Yes',
     'Yes', 'Yes', 'No', 'No',
     'No Churn', 4.20),

    -- Borderline customer
    ('Female', 1, 'No',  'No',  14,
     'One year', 'Yes', 'Credit card (automatic)', 65.00, 910.00,
     'Yes', 'No', 'DSL', 'No', 'Yes',
     'No', 'No', 'No', 'No',
     'No Churn', 38.60);
