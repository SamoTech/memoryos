# Security Policy

## Supported Versions

| Version | Supported |
|---|---|
| 1.0.x | ✅ Active |

## Reporting a Vulnerability

**Please do NOT open a public GitHub issue for security vulnerabilities.**

Use GitHub's private [Security Advisory](https://github.com/SamoTech/memoryos/security/advisories/new) feature to report vulnerabilities confidentially.

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Your suggested fix (if any)

You will receive a response within 48 hours. If confirmed, a patch will be released within 7 days and you will be credited in the release notes.

## Security Design

- API binds to `127.0.0.1` by default (not `0.0.0.0`)
- CORS restricted to `localhost` and `chrome-extension://`
- Extension communicates only with `localhost:8765`
- No authentication (single-user local tool by design)
- No telemetry, no external calls by default
- All data stored in `~/.memoryos/` (user-owned)

## Do NOT

- Expose port 8765 to the internet without authentication
- Share your `~/.memoryos/` directory
- Set `HOST=0.0.0.0` on a shared or public machine
