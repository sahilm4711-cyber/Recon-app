"""ReconX Step 2 runner: scope -> DNS -> passive subdomains -> report.

Usage: python3 main.py example.com
"""

import json
import sys

from reconx.scope import check_scope
from reconx.dns_lookup import dns_lookup
from reconx.subdomains import passive_subdomains


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
    dns = dns_lookup(domain)
    print(f"DNS status: {dns['status']}")
    print(f"A records: {dns['A']}")
    print("Target in scope, starting passive subdomain lookup (crt.sh)...")
    subs = passive_subdomains(domain)
    print(f"Subdomain status: {subs['status']}")
    if subs["status"] == "ok":
        print(f"Subdomains ({subs['count']}): {subs['subdomains']}")
        if subs["truncated"]:
            print("Note: list truncated at 500, see report for the flag.")
    else:
        print(f"Subdomain lookup failed, no fake list made: {subs['error']}")
    report = {"domain": domain, "dns": dns, "subdomains": subs}
    with open("report.json", "w") as f:
        json.dump(report, f, indent=2)
    print("Report saved locally: report.json")


if __name__ == "__main__":
    main()
