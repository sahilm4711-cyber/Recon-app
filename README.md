# ReconX - Step by Step

Big vision: ReconX v2.0 - full-stack web reconnaissance platform.
Now: Step 1 only - Scope + DNS, in small Python pieces, lab / authorised only.

## Step 1 - what this does
1. Scope check - is the target in the approved scope?
   - Approved scope for Step 1: example.com (lab target)
   - Anything else -> OUT_OF_SCOPE_TARGET, no scan, no save
2. DNS lookup - A / AAAA for an in-scope domain, using Python stdlib only
3. Report - prints a small report, saves it locally to report.json

## Run (on Kali / Termux, Python 3)
```
cd reconx
python3 main.py example.com
python3 main.py google.com   # should be rejected - out of scope
```

## Safety
Passive / public DNS only. No port scan, no personal data,
no other person's email / phone / username. Only authorised / lab targets.
