from log_parser import parse_logs
from translator import translate_logs
import json

sample = """
Jun 12 10:23:01 server sshd[1234]: Failed password for root from 192.168.1.105 port 22
Jun 12 10:23:03 server sshd[1234]: Failed password for root from 192.168.1.105 port 22
Jun 12 10:23:05 server sshd[1234]: Failed password for root from 192.168.1.105 port 22
Jun 12 10:24:01 server kernel: ERROR eth0: connection timeout to 10.0.0.1
Jun 12 10:24:45 server nginx: 502 Bad Gateway upstream connect() failed
Jun 12 10:25:01 server firewall: DENIED TCP 203.0.113.45 -> 192.168.1.1 port 3389
Jun 12 10:26:00 server kernel: WARNING memory usage exceeded 90% threshold
Jun 12 10:27:01 server sshd[5678]: Accepted publickey for admin from 10.0.0.5
"""

print("=== STEP 1: Parsing logs ===\n")
result = parse_logs(sample)

print(f"Total lines   : {result['total_lines']}")
print(f"Severity count: {result['severity_counts']}")
print(f"Anomalies     : {result['anomalies_detected']}")
print()
for item in result['parsed_lines']:
    print(f"  [{item['severity']:8}] {item['line'][:80]}")

print("\n=== STEP 2: Sending to Claude AI ===\n")
ai_result = translate_logs(result)
print(json.dumps(ai_result, indent=2))