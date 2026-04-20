# 🛡️ H2H Code Tech — AI Powered Network Log Translator

<div align="center">

![Project Banner](https://img.shields.io/badge/AI%20Powered-Network%20Log%20Translator-00d4ff?style=for-the-badge&logo=python&logoColor=white)

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?style=flat-square&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red?style=flat-square&logo=streamlit)
![Groq AI](https://img.shields.io/badge/Groq-LLaMA%203.3-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

**Translate raw network chaos into clear, actionable insights — powered by Groq AI**

[Features](#-features) • [Demo](#-demo) • [Setup](#-setup) • [Usage](#-usage) • [Tech Stack](#-tech-stack)

</div>

---

## 📌 What is this?

**AI Powered Network Log Translator** is an intelligent log analysis platform that takes raw, cryptic network logs and transforms them into human-readable insights using the power of Large Language Models.

No more spending hours deciphering logs manually. Paste your logs → Get instant AI analysis.

### What it does:
- 🗣 **Explains logs in Plain English** — no jargon, just clarity
- 🚨 **Detects Anomalies & Threats** — brute force, DDoS, port scans, firewall blocks
- 📊 **Summarizes Log Patterns** — understand recurring issues instantly
- ✅ **Suggests Fixes** — actionable next steps for every threat detected
- ⚡ **Severity Rating** — rates overall log health: LOW → CRITICAL

---

## 🎥 Demo

### Web Interface (FastAPI)
> Paste logs → Click Analyze → Get instant AI-powered insights

### Streamlit Dashboard
> Upload `.log` file → See metrics, anomalies, and suggestions in real time

---

## 📁 Project Structure

```
H2H-Code-Tech-AI-Powered-Network-Log-Translator/
│
├── backend/
│   ├── app.py                  # FastAPI web server
│   ├── log_parser.py           # Rule-based log parser
│   ├── translator.py           # Groq AI integration
│   └── requirements.txt        # Python dependencies
│
├── frontend/
│   ├── templates/
│   │   └── index.html          # Web UI
│   └── static/
│       ├── style.css           # Dark terminal styling
│       └── script.js           # Frontend logic
│
├── streamlit_app.py            # Streamlit dashboard
│
├── tests/
│   └── test_parser.py          # Unit tests
│
├── docs/
│   └── demo_instructions.md    # How to demo the project
│
├── README.md
└── .gitignore
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10+
- Groq API Key (free at [console.groq.com](https://console.groq.com))

### 1. Clone the repository

```bash
git clone https://github.com/nishamadhiyan/H2H-Code-Tech-AI-Powered-Network-Log-Translator.git
cd H2H-Code-Tech-AI-Powered-Network-Log-Translator
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the root folder:

```
GROQ_API_KEY=your_groq_api_key_here
```

Get your free API key at [console.groq.com](https://console.groq.com)

---

## ▶️ Running the App

### FastAPI Web App

```bash
cd backend
python app.py
```

Open browser at: `http://localhost:8000`

### Streamlit Dashboard

```bash
streamlit run streamlit_app.py
```

Open browser at: `http://localhost:8501`

---

## 🧪 Sample Logs to Try

Paste this into the app to test:

```
Jun 12 10:23:01 server sshd[1234]: Failed password for root from 192.168.1.105 port 22
Jun 12 10:23:03 server sshd[1234]: Failed password for root from 192.168.1.105 port 22
Jun 12 10:23:05 server sshd[1234]: Failed password for root from 192.168.1.105 port 22
Jun 12 10:24:01 server kernel: ERROR eth0: connection timeout to 10.0.0.1
Jun 12 10:24:45 server nginx: 502 Bad Gateway upstream connect() failed
Jun 12 10:25:01 server firewall: DENIED TCP 203.0.113.45 -> 192.168.1.1 port 3389
Jun 12 10:26:00 server kernel: WARNING memory usage exceeded 90% threshold
Jun 12 10:27:01 server sshd[5678]: Accepted publickey for admin from 10.0.0.5
```

### What you'll get:
- 🔴 **Severity:** MEDIUM
- 🚨 **Anomalies:** SSH Brute Force, Firewall Block, Memory Overload
- 🗣 **Summary:** Plain English explanation of what happened
- ✅ **Actions:** Step by step fix guide

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| AI Engine | Groq API (LLaMA 3.3 70B) |
| Backend | FastAPI + Uvicorn |
| Frontend | HTML / CSS / Vanilla JS |
| Dashboard | Streamlit |
| Log Parsing | Python (Regex-based) |
| Environment | python-dotenv |

---

## 🔍 How It Works

```
Raw Logs → log_parser.py → Severity Detection + Anomaly Rules
                        ↓
              translator.py → Groq AI (LLaMA 3.3)
                        ↓
         Plain English Summary + Severity + Suggestions
                        ↓
              Web UI / Streamlit Dashboard
```

---

## 🚨 Anomalies Detected

| Anomaly | Detection Method |
|---|---|
| SSH Brute Force | Repeated failed password attempts |
| DDoS / Flood | Flood/rate limit keywords |
| Firewall Block | Denied TCP/UDP patterns |
| Memory Overload | Memory exceeded threshold |
| Port Scan | Multiple port access from same IP |
| Repeated Failures | 3+ consecutive failures |

---

## 🔐 Security

- API keys are stored in `.env` — never committed to GitHub
- `.gitignore` excludes all sensitive files
- No user data is stored or logged

---

## 👥 Team

**H2H Code Tech**
- Built for Hackathon 2026
- Powered by Groq AI + FastAPI + Streamlit

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

<div align="center">
Made with ❤️ by H2H Code Tech | Powered by Groq AI
</div>