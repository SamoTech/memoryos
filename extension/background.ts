const API_BASE = 'http://localhost:8765';

interface PendingMemory {
  content: string;
  source: string;
  metadata?: Record<string, unknown>;
}

let queue: PendingMemory[] = [];
let flushTimer: ReturnType<typeof setTimeout> | null = null;

async function flushQueue() {
  if (queue.length === 0) return;
  const batch = [...queue];
  queue = [];
  try {
    const resp = await fetch(`${API_BASE}/api/v1/memories/bulk`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(batch),
    });
    if (resp.ok) {
      const saved = await resp.json();
      updateBadge(saved.length);
    }
  } catch {
    queue = [...batch, ...queue];
  }
}

function updateBadge(count: number) {
  chrome.storage.local.get(['totalCaptured'], (res) => {
    const total = (res.totalCaptured || 0) + count;
    chrome.storage.local.set({ totalCaptured: total });
    chrome.action.setBadgeText({ text: total > 99 ? '99+' : String(total) });
    chrome.action.setBadgeBackgroundColor({ color: '#6366f1' });
  });
}

chrome.runtime.onMessage.addListener((message) => {
  if (message.type === 'CAPTURE_MEMORY') {
    const payload = message.payload as PendingMemory;
    const isDupe = queue.some((q) => q.content === payload.content);
    if (!isDupe) {
      queue.push(payload);
      if (flushTimer) clearTimeout(flushTimer);
      flushTimer = setTimeout(flushQueue, 2000);
    }
  }
  return true;
});
