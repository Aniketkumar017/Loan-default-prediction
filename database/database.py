import sqlite3
import os
from datetime import datetime

# ==========================================================
# Database Path
# ==========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "loan_history.db")


# ==========================================================
# Create Database & Table
# ==========================================================

def initialize_database():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prediction_history(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        prediction_id TEXT UNIQUE,

        prediction_date TEXT,

        age INTEGER,

        income REAL,

        loan_amount REAL,

        credit_score INTEGER,

        probability REAL,

        risk_level TEXT

    )
    """)

    conn.commit()
    conn.close()


# ==========================================================
# Generate Prediction ID
# ==========================================================

def generate_prediction_id():

    initialize_database()

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM prediction_history")

    count = cursor.fetchone()[0] + 1

    conn.close()

    return f"LN-{count:06d}"


# ==========================================================
# Save Prediction
# ==========================================================

def save_prediction(
    age,
    income,
    loan_amount,
    credit_score,
    probability,
    risk_level
):

    initialize_database()

    prediction_id = generate_prediction_id()

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO prediction_history(

        prediction_id,
        prediction_date,
        age,
        income,
        loan_amount,
        credit_score,
        probability,
        risk_level

    )

    VALUES(?,?,?,?,?,?,?,?)

    """, (

        prediction_id,
        datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        age,
        income,
        loan_amount,
        credit_score,
        round(probability * 100, 2),
        risk_level

    ))

    conn.commit()
    conn.close()

    return prediction_id


# ==========================================================
# Get History
# ==========================================================

def get_history():

    initialize_database()

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM prediction_history

    ORDER BY id DESC

    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


# ==========================================================
# Delete One Prediction
# ==========================================================

def delete_prediction(prediction_id):

    initialize_database()

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""

    DELETE FROM prediction_history

    WHERE prediction_id = ?

    """, (prediction_id,))

    conn.commit()
    conn.close()


# ==========================================================
# Clear History
# ==========================================================

def clear_history():

    initialize_database()

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""

    DELETE FROM prediction_history

    """)

    conn.commit()
    conn.close()


# ==========================================================
# Get Total Predictions
# ==========================================================

def total_predictions():

    initialize_database()

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""

    SELECT COUNT(*)

    FROM prediction_history

    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


# ==========================================================
# Get Risk Counts
# ==========================================================

def risk_counts():

    initialize_database()

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""

    SELECT risk_level, COUNT(*)

    FROM prediction_history

    GROUP BY risk_level

    """)

    data = cursor.fetchall()

    conn.close()

    return data