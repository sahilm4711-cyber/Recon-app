"""ReconX Step 1 runner: scope -> DNS -> report.

Usage: python3 main.py example.com
"""
import json
import sys
from reconx.scope import check_scope
from reconx.dns_lookup import dns_lookup

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <domain>")
        print("Lab example: python3 main.py example.com")
        return
    ok, result = check_scope(sys.argv[1])
    if not ok:
        print(result)
        return
    domain = result
    print(f"Target: {domain} - in scope, starting passive DNS lookup...")
    report = dns_lookup(domain)
    print(f"Status: {report['status']}")
    print(f"A records: {report['A']}")
    print(f"AAAA records: {report['AAAA']}")
    with open("report.json", "w") as f:
        json.dump(report, f, indent=2)
    print("Report saved locally: report.json")

if __name__ == "__main__":
    main()
