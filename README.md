# 🛡️ NetLogAI — AI Powered Network Log Translator

> **Translate raw network chaos into clear, actionable insights — instantly.**

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?style=flat-square&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red?style=flat-square&logo=streamlit)
![Groq](https://img.shields.io/badge/Groq-LLaMA%203.3-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)
![Status](https://img.shields.io/badge/Status-Live-brightgreen?style=flat-square)

---

## 1. 📌 Project Title & Tagline

**NetLogAI** — The world's first free AI-powered network log translator that explains
raw network logs in plain English, detects security threats, and lets you
chat with your logs in real time.

---

## 2. 🚨 Problem Statement

Network and system logs are the most critical source of security intelligence —
but they are completely unreadable to most people.

**A typical network log looks like this:**
Jun 12 10:23:01 server sshd[1234]: Failed password for root from 192.168.1.105 port 22
Jun 12 10:24:45 server nginx: 502 Bad Gateway upstream connect() failed
Jun 12 10:25:01 server firewall: DENIED TCP 203.0.113.45 -> 192.168.1.1 port 3389

**Real-world problems this causes:**
- 🔴 Junior developers and non-technical staff cannot understand logs
- 🔴 Critical security threats go unnoticed because logs are too complex
- 🔴 Existing tools (Splunk, Datadog) cost $150–500/month
- 🔴 Setting up enterprise tools takes weeks of configuration
- 🔴 No free tool explains logs in simple human language
- 🔴 Sensitive data (passwords, tokens) often exposed in logs without masking

**Who faces this problem:**
- Small startups without dedicated security teams
- Junior developers learning DevOps and cybersecurity
- System administrators managing multiple servers
- Students and professionals learning network security

---

## 3. 💡 Proposed Solution

**NetLogAI** combines rule-based parsing with LLM intelligence to make
log analysis accessible to everyone — for free.

### What makes it unique:

| Feature | NetLogAI | Splunk | Datadog | Graylog |
|---|---|---|---|---|
| Plain English AI | ✅ | ❌ | ❌ | ❌ |
| Chat with logs | ✅ | ❌ | ❌ | ❌ |
| Free | ✅ | ❌ $150/mo | ❌ $15/host | ⚠️ Limited |
| Zero setup | ✅ | ❌ | ❌ | ❌ |
| Auto data masking | ✅ | 💰 Paid | 💰 Paid | ❌ |
| IP reputation check | ✅ | 💰 Paid | 💰 Paid | ❌ |
| Login/Register | ✅ | ✅ | ✅ | ✅ |
| Export reports | ✅ | ✅ | ✅ | ⚠️ |

### Our unique approach:
1. **Two-layer analysis** — Rule-based parser catches known patterns instantly,
   LLM explains context and nuance like a senior engineer
2. **Conversational AI** — First free log tool where you can ASK questions
   about your logs in natural language
3. **Privacy first** — Auto-masks passwords, tokens, emails before AI processing
4. **Dual interface** — FastAPI web UI for developers,
   Streamlit dashboard for non-technical users
5. **7-day history** — Analysis saved with expiry countdown and export option

---

## 4. 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| AI Engine | Groq API (LLaMA 3.3 70B) |
| Backend | FastAPI + Uvicorn |
| Frontend | HTML / CSS / Vanilla JS |
| Dashboard | Streamlit |
| Log Parsing | Python (Regex-based) |
| Database | SQLite |
| Charts | Chart.js |
| Authentication | JWT + bcrypt |
| Security | SlowAPI rate limiting |
| IP Intelligence | AbuseIPDB API |
| Environment | python-dotenv |
| Deployment | Render |

---

## 5. ✨ Features

- 🗣 **Plain English Translation** — Explains logs like a senior engineer
- 🚨 **Threat Detection** — SSH brute force, DDoS, port scans, firewall blocks
- 📊 **Visual Analytics** — Bar chart severity breakdown
- 💬 **Chat with Logs** — Ask AI questions about your specific logs
- 🌍 **IP Reputation Check** — Auto-checks suspicious IPs
- 📋 **Analysis History** — 7-day retention with expiry countdown
- 📥 **Export Reports** — Download full analysis as text report
- 🔐 **Auth System** — Login/Register with JWT tokens
- 🛡️ **Data Masking** — Auto-masks passwords, tokens, emails
- ⚡ **Rate Limiting** — Prevents API abuse
- 📁 **Large File Support** — Upload log files up to 50MB
- 🎯 **Sample Scenarios** — Pre-loaded attack samples
- 🔒 **Security Headers** — XSS and clickjacking protection
- 🌐 **Dual Interface** — Web app + Streamlit dashboard

---

## 6. 🔄 Architecture / Flow
┌─────────────────────────────────────────┐
│           User Interface                │
│   FastAPI Web UI  │  Streamlit Dashboard│
└────────────┬────────────────────────────┘
│
▼
┌─────────────────────────────────────────┐
│         Security Layer                  │
│  JWT Auth → Rate Limit → Input Validate │
│         → Data Masking                  │
└────────────┬────────────────────────────┘
│
▼
┌─────────────────────────────────────────┐
│      log_parser.py (Rule-based)         ││  Severity Detection (CRITICAL/ERROR/    │
│  WARNING/INFO) + Anomaly Detection      │
│  (Brute Force, DDoS, Port Scan)         │
└────────────┬────────────────────────────┘
│
▼
┌─────────────────────────────────────────┐
│     translator.py (AI Layer)            │
│     Groq API — LLaMA 3.3 70B           │
│  • Plain English Summary                │
│  • Severity Assessment                  │
│  • Pattern Analysis                     │
│  • Suggested Actions                    │
└────────────┬────────────────────────────┘
│
▼
┌─────────────────────────────────────────┐
│     IP Reputation Check                 │
│     AbuseIPDB API    └────────────┬────────────────────────────┘
│
▼
┌─────────────────────────────────────────┐
│     SQLite Database                     │
│     7-day retention + auto-delete       │
└─────────────────────────────────────────┘        ---

## 7. ⚙️ Setup Instructions

### Prerequisites
- Python 3.10+
- Groq API Key — free at [console.groq.com](https://console.groq.com)

### Step 1 — Clone the repository
```bash
git clone https://github.com/nishamadhiyan/H2H-Code-Tech-AI-Powered-Network-Log-Translator.git
cd H2H-Code-Tech-AI-Powered-Network-Log-Translator
```

### Step 2 — Install dependencies
```bash
pip install -r backend/requirements.txt
```

### Step 3 — Set up environment variables
Create a `.env` file in the root folder:    
GROQ_API_KEY=your_groq_api_key_here
SECRET_KEY=your-secret-key-here      

### Step 4 — Run FastAPI Web App
```bash
cd backend
python app.py
```
Open: **http://localhost:8000**

### Step 5 — Run Streamlit Dashboard (optional)
Open a new terminal:
```bash
streamlit run streamlit_app.py
```
Open: **http://localhost:8501**

### Default Login Credentials

### Step 5 — Run Streamlit Dashboard (optional)
Open a new terminal:
```bash
streamlit run streamlit_app.py
```
Open: **http://localhost:8501**

### Default Login Credentials
Username: admin
Password: admin123

---

## 8. 📸 Demo / Screenshots

### 🔐 Login Page
> Secure login and registration system with JWT authentication

### 🏠 Main Dashboard
> Paste logs or upload files — instant AI-powered analysis

### 📊 Analysis Results
> Severity badge, statistics, anomalies, AI summary

### 💬 Chat with Logs
> Ask questions about your logs in natural language

### 📱 Streamlit Dashboard
> Non-technical friendly interface with metrics and charts

### 🎥 Demo Video
> 📹 [Watch Full Demo on YouTube](#) — 3-5 minute walkthrough

---

## 9. 👥 Team Members

| Name | Role | GitHub |
|---|---|---|
| Nisha M | Full Stack + AI Integration | [@nishamadhiyan](https://github.com/nishamadhiyan) |
| [K M Kusuma] | Backend + Security | [@kmkusuma](https://github.kmkusuma) |

**Team:** H2H Code Tech
**Hackathon:** Hack2Hire 2026 — CSE Track

---

## 10. 🌐 Deployed Link

> 🔗 **Live App:** [https://h2h-code-tech-ai-powered-network-log-zd8s.onrender.com](#) — Deploy link coming soon

---

## 🔐 Security

- JWT authentication with 24-hour token expiry
- Rate limiting — 10 requests/minute per user
- Automatic sensitive data masking
- 7-day log retention with auto-delete
- File type and size validation — max 50MB
- Security headers — XSS and clickjacking protection

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

<div align="center">

**Made with ❤️ by H2H Code Tech**

Powered by Groq AI + FastAPI + Streamlit

*Built for Hack2Hire 2026*

</div>