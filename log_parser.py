import re

SEVERITY_PATTERNS = {
    "CRITICAL": r"\b(critical|fatal|panic|emergency)\b",
    "ERROR":    r"\b(error|err|failed|failure|refused|denied|unreachable)\b",
    "WARNING":  r"\b(warn|warning|timeout|retry|slow|high|exceeded)\b",
    "INFO":     r"\b(info|connected|established|success|accepted)\b",
}

ANOMALY_PATTERNS = {
    "SSH Brute Force":   r"(failed password|authentication failure).{0,100}(failed password|authentication failure)",
    "Port Scan":         r"(\d+\.\d+\.\d+\.\d+).{0,200}port\s+\d+.{0,200}port\s+\d+.{0,200}port\s+\d+",
    "DDoS / Flood":      r"\b(flood|ddos|bandwidth exceeded|rate limit)\b",
    "Firewall Block":    r"\b(denied|blocked|dropped).{0,50}(tcp|udp|icmp)\b",
    "Memory Overload":   r"\b(memory|ram).{0,50}(exceeded|full|critical|overflow)\b",
    "Repeated Failures": r"(failed|error|denied).{0,80}\n.{0,80}(failed|error|denied).{0,80}\n.{0,80}(failed|error|denied)",
}

def parse_logs(raw_text: str) -> dict:
    lines = [l.strip() for l in raw_text.strip().split("\n") if l.strip()]

    severity_counts = {"CRITICAL": 0, "ERROR": 0, "WARNING": 0, "INFO": 0, "UNKNOWN": 0}
    parsed_lines = []

    for line in lines:
        severity = "UNKNOWN"
        for level, pattern in SEVERITY_PATTERNS.items():
            if re.search(pattern, line, re.IGNORECASE):
                severity = level
                break
        severity_counts[severity] += 1
        parsed_lines.append({"line": line, "severity": severity})

    anomalies = []
    for name, pattern in ANOMALY_PATTERNS.items():
        if re.search(pattern, raw_text, re.IGNORECASE | re.MULTILINE):
            anomalies.append(name)

    return {
        "total_lines": len(lines),
        "severity_counts": severity_counts,
        "parsed_lines": parsed_lines,
        "anomalies_detected": anomalies,
        "raw": raw_text,
    }