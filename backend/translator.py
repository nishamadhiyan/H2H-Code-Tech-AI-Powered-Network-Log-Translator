import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

# Force reload env
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(env_path, override=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """
You are an expert network engineer and cybersecurity analyst.
Analyze the raw network logs provided and return ONLY a valid JSON object.
No markdown, no explanation outside the JSON, no backticks.

Return exactly this structure:
{
  "plain_english_summary": "2-3 sentence simple explanation of what happened",
  "severity_assessment": "LOW or MEDIUM or HIGH or CRITICAL",
  "anomalies": ["list of detected threats or anomalies"],
  "pattern_summary": "summary of recurring patterns in the logs",
  "suggested_actions": ["3 to 5 actionable steps to fix or investigate"],
  "key_events": ["top 3 to 5 most important log entries explained simply"]
}
"""

def translate_logs(parsed_data: dict) -> dict:
    raw_logs = parsed_data["raw"]

    user_message = f"""
Pre-analysis:
- Total log lines: {parsed_data['total_lines']}
- Severity breakdown: {parsed_data['severity_counts']}
- Rule-based anomalies found: {parsed_data['anomalies_detected']}

Raw logs:
{raw_logs[:4000]}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        max_tokens=1000,
        temperature=0.3
    )

    response_text = response.choices[0].message.content.strip()

    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if match:
            return json.loads(match.group())
        return {
            "plain_english_summary": "Could not parse AI response.",
            "severity_assessment": "UNKNOWN",
            "anomalies": [],
            "pattern_summary": "",
            "suggested_actions": [],
            "key_events": [],
            "raw_response": response_text
        }