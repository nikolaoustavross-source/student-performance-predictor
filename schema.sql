-- ============================================================
--  AIN5301EN – Introduction to AI
--  Assessment 2 – Student Performance Predictor
--  Database Schema (SQLite)
-- ============================================================
--  This schema stores prediction history so users can review
--  past results. Run once to initialise the database:
--
--    sqlite3 predictions.db < schema.sql
--
--  Or via Python:
--    import sqlite3
--    conn = sqlite3.connect('predictions.db')
--    conn.executescript(open('schema.sql').read())
-- ============================================================

-- Drop tables if they already exist (clean reset)
DROP TABLE IF EXISTS predictions;
DROP TABLE IF EXISTS feedback;

-- ──────────────────────────────────────────────────────────
--  TABLE: predictions
--  Stores every prediction made via the /predict endpoint.
-- ──────────────────────────────────────────────────────────
CREATE TABLE predictions (
    id                    INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Input features (mirrors the form in index.html)
    study_hours           REAL    NOT NULL,          -- e.g. 12.0
    attendance            REAL    NOT NULL,          -- 0–100 %
    previous_grade        REAL    NOT NULL,          -- 0–100
    assignments_submitted INTEGER NOT NULL,          -- count
    participation         TEXT    NOT NULL           -- Low / Medium / High
                          CHECK(participation IN ('Low', 'Medium', 'High')),

    -- Model output
    prediction            TEXT    NOT NULL           -- 'Pass' or 'Fail'
                          CHECK(prediction IN ('Pass', 'Fail')),
    probability           REAL    NOT NULL,          -- 0.00–100.00 %

    -- Metadata
    created_at            DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ──────────────────────────────────────────────────────────
--  TABLE: feedback
--  Optional — lets users confirm whether the prediction
--  was actually correct (useful for model improvement).
-- ──────────────────────────────────────────────────────────
CREATE TABLE feedback (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    prediction_id  INTEGER NOT NULL
                   REFERENCES predictions(id) ON DELETE CASCADE,
    actual_result  TEXT    NOT NULL
                   CHECK(actual_result IN ('Pass', 'Fail')),
    notes          TEXT,                             -- free-text comment
    created_at     DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ──────────────────────────────────────────────────────────
--  INDEXES — speed up common queries
-- ──────────────────────────────────────────────────────────

-- Look up predictions by outcome
CREATE INDEX idx_predictions_prediction ON predictions(prediction);

-- Look up predictions by date (e.g. recent history)
CREATE INDEX idx_predictions_created_at ON predictions(created_at);

-- Look up feedback by prediction
CREATE INDEX idx_feedback_prediction_id ON feedback(prediction_id);

-- ──────────────────────────────────────────────────────────
--  SAMPLE DATA — useful for testing
-- ──────────────────────────────────────────────────────────
INSERT INTO predictions
    (study_hours, attendance, previous_grade, assignments_submitted, participation, prediction, probability)
VALUES
    (10.0, 95.0, 85.0, 5, 'High',   'Pass', 97.50),
    (2.0,  40.0, 30.0, 1, 'Low',    'Fail', 91.20),
    (5.0,  65.0, 55.0, 2, 'Medium', 'Pass', 54.30);
