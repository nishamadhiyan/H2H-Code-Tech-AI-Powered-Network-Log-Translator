import sqlite3
import json
import os
from datetime import datetime, timedelta

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
            summary TEXT,
            expires_at TEXT
        )
    ''')
    conn.commit()
    conn.close()
    delete_expired_logs()

def delete_expired_logs():
    conn = sqlite3.connect(DB_PATH)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute("DELETE FROM analyses WHERE expires_at < ?", (now,))
    conn.commit()
    conn.close()

def save_analysis(parsed: dict, ai_result: dict, keep_days: int = 7):
    delete_expired_logs()
    expires_at = (datetime.now() + timedelta(days=keep_days)).strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        INSERT INTO analyses 
        (timestamp, total_lines, severity, anomalies, summary, expires_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        parsed["total_lines"],
        ai_result.get("severity_assessment", "UNKNOWN"),
        json.dumps(ai_result.get("anomalies", [])),
        ai_result.get("plain_english_summary", "")[:200],
        expires_at
    ))
    conn.commit()
    conn.close()

def get_history():
    delete_expired_logs()
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
            "summary": r[5],
            "expires_at": r[6],
            "days_left": max(0, (
                datetime.strptime(r[6], "%Y-%m-%d %H:%M:%S") - datetime.now()
            ).days)
        }
        for r in rows
    ]