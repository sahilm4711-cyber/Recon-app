"""Step 1, piece 2: DNS lookup, stdlib only.

Logic: socket.getaddrinfo asks the system DNS resolver for a name.
It returns IP addresses. We dedup them, split IPv4 (A) and IPv6 (AAAA).
No direct connection to the target is made - this is a DNS lookup only.
"""
import socket

def dns_lookup(domain: str):
    try:
        infos = socket.getaddrinfo(domain, None)
    except socket.gaierror as e:
        return {"domain": domain, "status": "failed", "error": str(e), "A": [], "AAAA": []}
    a, aaaa = set(), set()
    for info in infos:
        family, _, _, _, sockaddr = info
        ip = sockaddr[0]
        if family == socket.AF_INET:
            a.add(ip)
        elif family == socket.AF_INET6:
            aaaa.add(ip)
    return {"domain": domain, "status": "ok", "A": sorted(a), "AAAA": sorted(aaaa)}
