"""Step 1, piece 1: scope check.

Logic, in plain words:
- Normalise: lower-case, strip spaces, strip a trailing dot.
- Validate: a domain must look like name.name, letters/digits/hyphens only.
- Scope: a target is in scope only if it IS an approved domain,
  or a subdomain of an approved domain.
- Out of scope: return an OUT_OF_SCOPE error, and the caller must NOT scan.
"""
import re

APPROVED_SCOPE = ["example.com"]  # Lab target for Step 1

DOMAIN_RE = re.compile(r"^(?!-)[a-z0-9-]{1,63}(?<!-)(\.[a-z0-9-]{1,63})+$")

def normalize(domain: str) -> str:
    return domain.strip().lower().rstrip(".")

def is_valid_domain(domain: str) -> bool:
    return bool(DOMAIN_RE.match(domain))

def is_in_scope(domain: str, scope=None) -> bool:
    scope = scope or APPROVED_SCOPE
    domain = normalize(domain)
    for approved in scope:
        approved = normalize(approved)
        if domain == approved or domain.endswith("." + approved):
            return True
    return False

def check_scope(domain: str):
    """Returns (ok, message_or_error_dict)."""
    domain = normalize(domain)
    if not is_valid_domain(domain):
        return False, {"error": "INVALID_DOMAIN", "target": domain, "scan_started": False}
    if not is_in_scope(domain):
        return False, {
            "error": "OUT_OF_SCOPE_TARGET",
            "message": "The requested target is not included in the verified project scope.",
            "target": domain,
            "scan_started": False,
        }
    return True, domain
