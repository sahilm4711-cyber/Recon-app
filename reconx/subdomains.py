"""ReconX Step 2: passive subdomains from public certificate logs.

Logic, in plain words:
- Source: crt.sh Certificate Transparency search (public records only).
  We never connect to the target itself in this step, and we never
  brute-force names - we only read names that already appear in
  public certificates for the in-scope domain.
- Parse: each crt.sh entry has a name_value field, sometimes with
  several names on separate lines, sometimes starting with "*.".
  Strip "*.", lower-case, keep only names that are the approved
  domain or a subdomain of it, drop the domain itself (that is not
  a subdomain), remove duplicates, sort.
- Cap: at most 500 subdomains, matching ReconX v2.0 FR-04.
  If there are more, keep the first 500 and report truncated=True,
  never silently drop the rest without saying so.
- Failure: if crt.sh cannot be reached, return status "failed"
  with the error, and no fake subdomain list. The caller saves
  that honest result instead of inventing one.
"""

import json
import urllib.request

CRT_SH_URL = "https://crt.sh/?q=%25.{domain}&output=json"
MAX_SUBDOMAINS = 500


def parse_entries(entries, domain):
    """Pure parsing step - easy to test without any network call."""
    domain = domain.strip().lower().rstrip(".")
    found = set()
    for entry in entries:
        for raw in str(entry.get("name_value", "")).splitlines():
            name = raw.strip().lower().lstrip("*.")
            if not name or name == domain:
                continue
            if name.endswith("." + domain):
                found.add(name)
    ordered = sorted(found)
    truncated = len(ordered) > MAX_SUBDOMAINS
    return ordered[:MAX_SUBDOMAINS], truncated


def passive_subdomains(domain):
    """Fetch and parse passive subdomains for an in-scope domain.

    Callers must check scope first (reconx.scope.check_scope) and
    must not call this for an out-of-scope target.
    """
    domain = domain.strip().lower().rstrip(".")
    url = CRT_SH_URL.format(domain=domain)
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "ReconX-lab/Step2"}
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            entries = json.load(resp)
    except Exception as exc:  # network / service failure: report, don't invent
        return {
            "domain": domain,
            "source": "crt.sh",
            "status": "failed",
            "error": f"{type(exc).__name__}: {exc}",
            "subdomains": [],
            "count": 0,
            "truncated": False,
        }
    subdomains, truncated = parse_entries(entries, domain)
    return {
        "domain": domain,
        "source": "crt.sh",
        "status": "ok",
        "subdomains": subdomains,
        "count": len(subdomains),
        "truncated": truncated,
    }
