"""Step 3: runtime scope - any domain, with permission confirmation.

Logic, in plain words:
- Step 1-2 hard-coded scope (example.com only) is removed.
- Now the user types any domain at run time.
- Two checks must pass, in order:
  1. Domain syntax must be valid.
  2. Permission must be confirmed: "I own this domain, or I have
     written permission to test it." Without that, no lookup runs.
- This step does NOT verify ownership (DNS TXT verification is a
  later ReconX v2.0 step). The confirmation is the user's
  responsibility: only use domains you own or have written
  permission for. The app still does passive checks only.
- Out-of-scope is now replaced by PERMISSION_NOT_CONFIRMED.
"""
import re

DOMAIN_RE = re.compile(r"^(?!-)[a-z0-9-]{1,63}(?<!-)(\.[a-z0-9-]{1,63})+$")

def normalize(domain: str) -> str:
    return domain.strip().lower().rstrip(".")

def is_valid_domain(domain: str) -> bool:
    return bool(DOMAIN_RE.match(domain))

def check_scope(domain: str, confirmed: bool = False):
    """Returns (ok, message_or_domain)."""
    domain = normalize(domain)
    if not is_valid_domain(domain):
        return False, {"error": "INVALID_DOMAIN", "target": domain, "scan_started": False}
    if not confirmed:
        return False, {
            "error": "PERMISSION_NOT_CONFIRMED",
            "message": "Confirm you own this domain, or have written permission to test it, before any lookup.",
            "target": domain,
            "scan_started": False,
        }
    return True, domain
