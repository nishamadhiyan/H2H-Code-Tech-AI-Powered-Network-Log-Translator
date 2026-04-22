import requests
import os
import re
from dotenv import load_dotenv
load_dotenv()

def extract_ips(text: str) -> list:
    pattern = r'\b(?!10\.|192\.168\.|172\.(1[6-9]|2[0-9]|3[0-1])\.)(\d{1,3}\.){3}\d{1,3}\b'
    return list(set(re.findall(r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b', text)))

def check_ip_reputation(ip: str) -> dict:
    try:
        api_key = os.getenv("ABUSEIPDB_API_KEY")
        if not api_key:
            return {"ip": ip, "error": "No API key"}

        response = requests.get(
            "https://api.abuseipdb.com/api/v2/check",
            headers={"Key": api_key, "Accept": "application/json"},
            params={"ipAddress": ip, "maxAgeInDays": 90},
            timeout=5
        )
        data = response.json().get("data", {})
        return {
            "ip": ip,
            "abuse_score": data.get("abuseConfidenceScore", 0),
            "country": data.get("countryCode", "Unknown"),
            "total_reports": data.get("totalReports", 0),
            "is_malicious": data.get("abuseConfidenceScore", 0) > 25,
            "isp": data.get("isp", "Unknown")
        }
    except:
        return {"ip": ip, "error": "Check failed"}

def check_all_ips(log_text: str) -> list:
    ips = extract_ips(log_text)
    results = []
    for ip in ips[:5]:
        results.append(check_ip_reputation(ip))
    return results