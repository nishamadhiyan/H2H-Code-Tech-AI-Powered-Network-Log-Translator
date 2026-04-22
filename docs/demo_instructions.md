# Demo Instructions

## How to Run

### FastAPI Web App
```bash
cd backend
python app.py
```
Open: http://localhost:8000

### Streamlit App
```bash
streamlit run streamlit_app.py
```
Open: http://localhost:8501

## Demo Scenarios

### Scenario 1 — SSH Brute Force
- Click "Load Brute Force Sample"
- Click Analyze
- Shows: HIGH severity, SSH Brute Force detected

### Scenario 2 — DDoS Attack
- Click "Load DDoS Sample"
- Click Analyze
- Shows: HIGH severity, DDoS/Flood detected

### Scenario 3 — Memory Overload
- Click "Load Memory Overload Sample"
- Click Analyze
- Shows: CRITICAL severity, Memory Overload detected

## Features to Show
1. Plain English Summary
2. Severity Badge
3. Log Statistics
4. Anomaly Detection
5. Suggested Actions
6. Click any log line for AI explanation
7. Export Report button