const SOURCE = 'gemini';
const SENT_HASHES = new Set<string>();

function hash(str: string): string {
  let h = 0;
  for (let i = 0; i < str.length; i++) h = (Math.imul(31, h) + str.charCodeAt(i)) | 0;
  return String(h);
}

function extractAndSend() {
  const queries = document.querySelectorAll('.query-text, [class*="user-query"]');
  const responses = document.querySelectorAll('model-response, [class*="model-response"]');
  const len = Math.min(queries.length, responses.length);
  for (let i = 0; i < len; i++) {
    const user = (queries[i] as HTMLElement).innerText.trim();
    const assistant = (responses[i] as HTMLElement).innerText.trim();
    if (!user || !assistant) continue;
    const content = `User: ${user}\n\nAssistant: ${assistant}`;
    const key = hash(content);
    if (SENT_HASHES.has(key)) continue;
    SENT_HASHES.add(key);
    chrome.runtime.sendMessage({
      type: 'CAPTURE_MEMORY',
      payload: { content, source: SOURCE, metadata: { url: location.href } },
    });
  }
}

new MutationObserver(() => extractAndSend())
  .observe(document.body, { childList: true, subtree: true });
extractAndSend();
