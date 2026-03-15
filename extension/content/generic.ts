// Generic fallback scraper — disabled by default, user must enable per-site
const SOURCE = 'api';
const SENT_HASHES = new Set<string>();

function hash(str: string): string {
  let h = 0;
  for (let i = 0; i < str.length; i++) h = (Math.imul(31, h) + str.charCodeAt(i)) | 0;
  return String(h);
}

chrome.storage.sync.get(['genericEnabled', 'enabledHosts'], (config) => {
  const enabledHosts: string[] = config.enabledHosts || [];
  if (!config.genericEnabled && !enabledHosts.includes(location.hostname)) return;

  function tryCapture() {
    const aiSelectors = [
      '[class*="message"]', '[class*="response"]',
      '[class*="assistant"]', '[class*="chat"]',
      'article', '.prose',
    ];
    for (const sel of aiSelectors) {
      const els = document.querySelectorAll(sel);
      if (els.length > 2) {
        els.forEach((el) => {
          const text = (el as HTMLElement).innerText?.trim();
          if (!text || text.length < 50) return;
          const key = hash(text);
          if (SENT_HASHES.has(key)) return;
          SENT_HASHES.add(key);
          chrome.runtime.sendMessage({
            type: 'CAPTURE_MEMORY',
            payload: { content: text, source: SOURCE, metadata: { url: location.href } },
          });
        });
        return;
      }
    }
  }

  new MutationObserver(tryCapture).observe(document.body, { childList: true, subtree: true });
});
