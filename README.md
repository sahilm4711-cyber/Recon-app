# ReconX - Step by Step

Big vision: ReconX v2.0 - full-stack web reconnaissance platform.
Now: Steps 1-2 only - Scope + DNS + passive subdomains, in small Python pieces, lab / authorised only.

## Step 1 - Scope + DNS
1. Scope check - is the target in the approved scope?
   - Approved scope: example.com (lab target)
   - Anything else -> OUT_OF_SCOPE_TARGET, no scan, no save
2. DNS lookup - A / AAAA for an in-scope domain, using Python stdlib only

## Step 2 - Passive subdomains (new)
3. Subdomain lookup - from crt.sh public Certificate Transparency records only.
   No brute-forcing, no direct connection to the target.
   Wildcard entries are cleaned, duplicates removed, out-of-scope names dropped,
   the domain itself is not counted as a subdomain, at most 500 kept.
4. Report - prints DNS + subdomains, saves them locally to report.json only.
   If crt.sh cannot be reached, the report says "failed" - it never invents a list.

## Run (on Kali / Termux, Python 3)
```
python3 main.py example.com
python3 main.py google.com   # should be rejected - out of scope, before any lookup
```

## Safety
Passive / public records only. No port scan, no personal data,
no other person's email / phone / username. Only authorised / lab targets.

## Real web application (new)
```
python3 server.py
```
Then open http://127.0.0.1:8000
- Target: example.com, tick the permission checkbox, Start passive recon
- See DNS + passive subdomains in the browser, download report as JSON (local only)
- Out-of-scope targets get 403 OUT_OF_SCOPE_TARGET, no scan
- Files: server.py (stdlib only, no pip install), web/index.html, web/style.css, web/app.js
