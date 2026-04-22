import streamlit as st
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
from log_parser import parse_logs
from translator import translate_logs

st.set_page_config(
    page_title="AI Network Log Translator",
    page_icon="🛡️",
    layout="wide"
)

st.markdown("""
<style>
.main { background-color: #0a0f1e; }
.stApp { background-color: #0a0f1e; color: #c9d8f0; }
h1 { color: #00d4ff !important; }
h2, h3 { color: #00d4ff !important; }
.stTextArea textarea { background-color: #0f1629 !important; color: #c9d8f0 !important; border: 1px solid #1e3a5f !important; }
.stButton button { background: linear-gradient(135deg, #00d4ff, #0077ff) !important; color: #000 !important; font-weight: bold !important; border: none !important; }
.stMetric { background-color: #0f1629 !important; border: 1px solid #1e3a5f !important; border-radius: 8px !important; padding: 10px !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center'>⬡ NetLogAI — Network Log Translator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#4a6080;letter-spacing:2px'>TRANSLATE CHAOS INTO CLARITY — INSTANTLY</p>", unsafe_allow_html=True)
st.divider()

SAMPLES = {
    "🔴 SSH Brute Force": """Jun 12 10:23:01 server sshd[1234]: Failed password for root from 192.168.1.105 port 22
Jun 12 10:23:03 server sshd[1234]: Failed password for root from 192.168.1.105 port 22
Jun 12 10:23:05 server sshd[1234]: Failed password for root from 192.168.1.105 port 22
Jun 12 10:23:07 server sshd[1234]: Failed password for root from 192.168.1.105 port 22
Jun 12 10:23:09 server sshd[1234]: Failed password for root from 192.168.1.105 port 22""",

    "🟠 DDoS Attack": """Jun 12 11:00:01 server kernel: WARNING flood detected from 45.33.32.156
Jun 12 11:00:02 server firewall: DENIED TCP 45.33.32.156 -> 192.168.1.1 port 80
Jun 12 11:00:03 server nginx: rate limit exceeded for 45.33.32.156
Jun 12 11:00:04 server kernel: DDoS attack detected bandwidth exceeded
Jun 12 11:00:05 server firewall: DROPPED UDP 45.33.32.156 -> 192.168.1.1""",

    "🟡 Memory Overload": """Jun 12 12:00:01 server kernel: WARNING memory usage exceeded 90% threshold
Jun 12 12:00:05 server kernel: CRITICAL memory usage exceeded 95% threshold
Jun 12 12:00:10 server kernel: ERROR out of memory killing process nginx
Jun 12 12:00:15 server kernel: CRITICAL RAM overflow detected
Jun 12 12:00:20 server app: fatal memory allocation failed"""
}

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📋 Input Logs")

    sample_choice = st.selectbox("Load a sample scenario", ["None"] + list(SAMPLES.keys()))

    default_text = SAMPLES[sample_choice] if sample_choice != "None" else ""
    log_text = st.text_area("Or paste your logs here", value=default_text, height=250,
        placeholder="Paste raw network logs here...")

    uploaded = st.file_uploader("Or upload a .log / .txt file", type=["log", "txt"])
    if uploaded:
        log_text = uploaded.read().decode("utf-8", errors="ignore")
        st.success(f"✅ Loaded: {uploaded.name}")

    analyze_btn = st.button("⚡ Analyze Logs", use_container_width=True)

with col2:
    if analyze_btn and log_text.strip():
        with st.spinner("🤖 AI is analyzing your logs..."):
            parsed = parse_logs(log_text)
            result = translate_logs(parsed)

        sev = result.get("severity_assessment", "UNKNOWN")
        sev_emoji = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🟢"}.get(sev, "⚪")

        st.subheader("📊 Analysis Results")
        st.markdown(f"### {sev_emoji} Severity: `{sev}`")
        st.info(result.get("plain_english_summary", "—"))

        sc = parsed["severity_counts"]
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("📝 Total", parsed["total_lines"])
        m2.metric("🔴 Critical", sc.get("CRITICAL", 0))
        m3.metric("🟠 Errors", sc.get("ERROR", 0))
        m4.metric("🟡 Warnings", sc.get("WARNING", 0))
        m5.metric("🟢 Info", sc.get("INFO", 0))

        st.divider()

        anomalies = list(set(
            parsed.get("anomalies_detected", []) + result.get("anomalies", [])
        ))
        if anomalies:
            st.error("🚨 Anomalies: " + " | ".join(anomalies))
        else:
            st.success("✅ No anomalies detected")

        with st.expander("🔍 Pattern Summary"):
            st.write(result.get("pattern_summary", "—"))

        with st.expander("🔑 Key Events"):
            for e in result.get("key_events", []):
                st.markdown(f"- {e}")

        with st.expander("✅ Suggested Actions"):
            for a in result.get("suggested_actions", []):
                st.markdown(f"- {a}")

        with st.expander("📄 Log Lines by Severity"):
            colors = {"CRITICAL": "🔴", "ERROR": "🟠", "WARNING": "🟡", "INFO": "🟢", "UNKNOWN": "⚪"}
            for item in parsed["parsed_lines"]:
                st.markdown(f"{colors.get(item['severity'], '⚪')} `[{item['severity']}]` {item['line']}")

        st.divider()
        report = f"""
AI NETWORK LOG TRANSLATOR — REPORT
====================================
Severity: {sev}
Total Lines: {parsed['total_lines']}

SUMMARY
-------
{result.get('plain_english_summary', '')}

ANOMALIES
---------
{chr(10).join(anomalies)}

PATTERN SUMMARY
---------------
{result.get('pattern_summary', '')}

KEY EVENTS
----------
{chr(10).join(result.get('key_events', []))}

SUGGESTED ACTIONS
-----------------
{chr(10).join(result.get('suggested_actions', []))}
        """.strip()

        st.download_button(
            label="📥 Export Report",
            data=report,
            file_name="network-log-report.txt",
            mime="text/plain",
            use_container_width=True
        )

    elif analyze_btn:
        st.warning("Please provide some log input first.")
    else:
        st.markdown("""
        ### 👈 Paste logs or pick a sample to get started

        This tool will:
        - 🗣 **Explain** what happened in plain English
        - 🚨 **Detect** threats and anomalies
        - 📊 **Summarize** log patterns
        - ✅ **Suggest** actions to take
        - 📥 **Export** a full report
        """)