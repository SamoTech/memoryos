const SOURCE = 'chatgpt';
const SENT_HASHES = new Set<string>();

function hash(str: string): string {
  let h = 0;
  for (let i = 0; i < str.length; i++) {
    h = (Math.imul(31, h) + str.charCodeAt(i)) | 0;
  }
  return String(h);
}

function extractAndSend() {
  const turns = document.querySelectorAll('[data-message-author-role]');
  const pairs: { user: string; assistant: string }[] = [];
  let currentUser = '';

  turns.forEach((el) => {
    const role = el.getAttribute('data-message-author-role');
    const text = (el as HTMLElement).innerText.trim();
    if (!text) return;
    if (role === 'user') {
      currentUser = text;
    } else if (role === 'assistant' && currentUser) {
      pairs.push({ user: currentUser, assistant: text });
      currentUser = '';
    }
  });

  for (const { user, assistant } of pairs) {
    const content = `User: ${user}\n\nAssistant: ${assistant}`;
    const key = hash(content);
    if (SENT_HASHES.has(key)) continue;
    SENT_HASHES.add(key);
    chrome.runtime.sendMessage({
      type: 'CAPTURE_MEMORY',
      payload: {
        content,
        source: SOURCE,
        metadata: { url: location.href, title: document.title },
      },
    });
    showCaptureIndicator();
  }
}

function showCaptureIndicator() {
  const dot = document.createElement('div');
  dot.style.cssText = [
    'position:fixed', 'bottom:24px', 'right:24px', 'width:10px', 'height:10px',
    'border-radius:50%', 'background:#22c55e', 'z-index:99999',
    'opacity:1', 'transition:opacity 2s',
  ].join(';');
  document.body.appendChild(dot);
  setTimeout(() => { dot.style.opacity = '0'; }, 500);
  setTimeout(() => dot.remove(), 2500);
}

const observer = new MutationObserver(() => extractAndSend());
observer.observe(document.body, { childList: true, subtree: true });
extractAndSend();
