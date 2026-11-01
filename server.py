"""ReconX Web - real web application, Step 1-2 as a web app.

Run: python3 server.py
Then open: http://127.0.0.1:8000

Stdlib only - no pip install needed, so it runs on Kali with python3 alone.
API: GET /api/scan?domain=example.com
  - scope checked first, out-of-scope -> 403 OUT_OF_SCOPE_TARGET, no scan
  - in-scope -> DNS (stdlib) + passive subdomains (crt.sh, public records)
  - report is returned as JSON, saved nowhere on a server (this is local)
Safety: lab / authorised only, passive only, no personal data.
"""
import json
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

sys.path.insert(0, str(Path(__file__).parent.parent / "reconx"))
# Fallback: if run from inside the repo copy, import from local reconx package
try:
    from reconx.scope import check_scope
    from reconx.dns_lookup import dns_lookup
    from reconx.subdomains import passive_subdomains
except ImportError:
    # When server.py lives in the same repo root as reconx/
    sys.path.insert(0, str(Path(__file__).parent))
    from reconx.scope import check_scope
    from reconx.dns_lookup import dns_lookup
    from reconx.subdomains import passive_subdomains

WEB_DIR = Path(__file__).parent / "web"

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)
    def log_message(self, *args):
        pass
    def send_json(self, data, status=200):
        body = json.dumps(data, indent=2).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/scan":
            domain = parse_qs(parsed.query).get("domain", [""])[0]
            ok, result = check_scope(domain)
            if not ok:
                self.send_json(result, status=403)
                return
            domain = result
            dns = dns_lookup(domain)
            subs = passive_subdomains(domain)
            self.send_json({"domain": domain, "dns": dns, "subdomains": subs})
            return
        if parsed.path == "/":
            self.path = "/index.html"
        return super().do_GET()

if __name__ == "__main__":
    print("ReconX Web running at http://127.0.0.1:8000  (Ctrl+C to stop)")
    ThreadingHTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
