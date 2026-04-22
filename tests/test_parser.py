import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))
from log_parser import parse_logs

def test_severity_detection():
    logs = "Jun 12 server: ERROR connection failed"
    result = parse_logs(logs)
    assert result["severity_counts"]["ERROR"] == 1
    print("✅ test_severity_detection passed")

def test_anomaly_detection():
    logs = """Failed password from 192.168.1.1 port 22
Failed password from 192.168.1.1 port 22
Failed password from 192.168.1.1 port 22
Failed password from 192.168.1.1 port 22
Failed password from 192.168.1.1 port 22"""
    result = parse_logs(logs)
    assert len(result["anomalies_detected"]) > 0
    print("✅ test_anomaly_detection passed")

def test_total_lines():
    logs = "line one\nline two\nline three"
    result = parse_logs(logs)
    assert result["total_lines"] == 3
    print("✅ test_total_lines passed")

def test_warning_detection():
    logs = "Jun 12 server: WARNING memory exceeded threshold"
    result = parse_logs(logs)
    assert result["severity_counts"]["WARNING"] == 1
    print("✅ test_warning_detection passed")

def test_info_detection():
    logs = "Jun 12 server: connection established successfully"
    result = parse_logs(logs)
    assert result["severity_counts"]["INFO"] == 1
    print("✅ test_info_detection passed")

if __name__ == "__main__":
    print("\n🧪 Running all tests...\n")
    test_severity_detection()
    test_anomaly_detection()
    test_total_lines()
    test_warning_detection()
    test_info_detection()
    print("\n🎉 All tests passed!\n")