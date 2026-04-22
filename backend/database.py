import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'history.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            total_lines INTEGER,
            severity TEXT,
            anomalies TEXT,
            summary TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_analysis(parsed: dict, ai_result: dict):
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        INSERT INTO analyses (timestamp, total_lines, severity, anomalies, summary)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        parsed["total_lines"],
        ai_result.get("severity_assessment", "UNKNOWN"),
        json.dumps(ai_result.get("anomalies", [])),
        ai_result.get("plain_english_summary", "")[:200]
    ))
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        'SELECT * FROM analyses ORDER BY id DESC LIMIT 20'
    ).fetchall()
    conn.close()
    return [
        {
            "id": r[0],
            "timestamp": r[1],
            "total_lines": r[2],
            "severity": r[3],
            "anomalies": json.loads(r[4]),
            "summary": r[5]
        }
        for r in rows
    ]