"""ReconX Step 3 runner: permission -> DNS -> passive subdomains -> report.

Usage: python3 main.py example.com
The runner asks: do you own this domain, or have written permission?
Answer yes to continue, anything else stops before any lookup.
"""
import json
import sys
from reconx.scope import check_scope
from reconx.dns_lookup import dns_lookup
from reconx.subdomains import passive_subdomains

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <domain>")
        print("Example (lab): python3 main.py example.com")
        return
    target = sys.argv[1]
    answer = input(f"Do you own {target}, or have written permission to test it? (yes/no): ").strip().lower()
    confirmed = answer in ("yes", "y")
    ok, result = check_scope(target, confirmed=confirmed)
    if not ok:
        print(result)
        return
    domain = result
    print(f"Target: {domain} - permission confirmed, starting passive DNS lookup...")
    dns = dns_lookup(domain)
    print(f"DNS status: {dns['status']}")
    print(f"A records: {dns['A']}")
    print("Starting passive subdomain lookup (crt.sh)...")
    subs = passive_subdomains(domain)
    print(f"Subdomain status: {subs['status']}")
    if subs["status"] == "ok":
        print(f"Subdomains ({subs['count']}): {subs['subdomains']}")
    else:
        print(f"Subdomain lookup failed, no fake list made: {subs['error']}")
    report = {"domain": domain, "dns": dns, "subdomains": subs}
    with open("report.json", "w") as f:
        json.dump(report, f, indent=2)
    print("Report saved locally: report.json")

if __name__ == "__main__":
    main()
