const API = 'http://localhost:8765';

const searchInput = document.getElementById('search') as HTMLInputElement;
const resultsEl = document.getElementById('results') as HTMLDivElement;
const statusDot = document.getElementById('status-dot') as HTMLSpanElement;
const captureToggle = document.getElementById('capture-toggle') as HTMLInputElement;
const openDashboard = document.getElementById('open-dashboard') as HTMLAnchorElement;

openDashboard.addEventListener('click', (e) => {
  e.preventDefault();
  chrome.tabs.create({ url: 'http://localhost:3000' });
});

async function checkHealth() {
  try {
    const resp = await fetch(`${API}/health`, { signal: AbortSignal.timeout(2000) });
    if (resp.ok) {
      statusDot.className = 'dot online';
      statusDot.title = 'Server online';
      loadRecent();
      return;
    }
  } catch {}
  statusDot.className = 'dot offline';
  statusDot.title = 'Server offline';
  renderEmpty('Server offline. Run: memoryos start');
}

async function loadRecent() {
  try {
    const resp = await fetch(`${API}/api/v1/memories?limit=5`);
    const memories = await resp.json();
    renderResults(memories.map((m: any) => ({ memory: m, score: 1 })));
  } catch {}
}

async function doSearch(q: string) {
  if (!q.trim()) { loadRecent(); return; }
  try {
    const resp = await fetch(`${API}/api/v1/search?q=${encodeURIComponent(q)}&limit=8`);
    const results = await resp.json();
    renderResults(results);
  } catch { renderEmpty('Search failed.'); }
}

function renderResults(items: any[]) {
  if (!items.length) { renderEmpty('No memories found.'); return; }
  resultsEl.innerHTML = items.map((item) => {
    const m = item.memory;
    const text = m.summary || m.content;
    return `
      <div class="result-item">
        <div class="result-source">${m.source}</div>
        <div class="result-text">${escHtml(text)}</div>
      </div>`;
  }).join('');
}

function renderEmpty(msg: string) {
  resultsEl.innerHTML = `<div class="empty">${msg}</div>`;
}

function escHtml(str: string) {
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

let debounce: ReturnType<typeof setTimeout>;
searchInput.addEventListener('input', () => {
  clearTimeout(debounce);
  debounce = setTimeout(() => doSearch(searchInput.value), 300);
});

chrome.storage.sync.get(['captureEnabled'], (res) => {
  captureToggle.checked = res.captureEnabled !== false;
});
captureToggle.addEventListener('change', () => {
  chrome.storage.sync.set({ captureEnabled: captureToggle.checked });
});

checkHealth();
