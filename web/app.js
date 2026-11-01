// ReconX Web frontend - calls the local /api/scan endpoint, nothing else.
const form = document.getElementById('scanForm');
const statusEl = document.getElementById('status');
const resultsEl = document.getElementById('results');
let lastReport = null;
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const domain = document.getElementById('domain').value.trim();
  statusEl.textContent = 'Running passive recon...';
  resultsEl.hidden = true;
  const res = await fetch('/api/scan?domain=' + encodeURIComponent(domain) + '&confirm=true');
  const data = await res.json();
  lastReport = data;
  if (!res.ok) {
    statusEl.textContent = 'Rejected: ' + (data.error || 'error') + ' - ' + (data.message || data.target || '');
    return;
  }
  statusEl.textContent = 'Done for ' + data.domain;
  document.getElementById('dns').textContent = JSON.stringify(data.dns, null, 2);
  document.getElementById('subs').textContent = JSON.stringify(data.subdomains, null, 2);
  resultsEl.hidden = false;
});
document.getElementById('download').addEventListener('click', () => {
  const blob = new Blob([JSON.stringify(lastReport, null, 2)], {type: 'application/json'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'reconx-report.json';
  a.click();
});
