import subprocess
import sys
import webbrowser
import signal
import os
import json
from pathlib import Path

import click
import requests

DATA_DIR = Path.home() / ".memoryos"
PID_FILE = DATA_DIR / "server.pid"
API_BASE = "http://127.0.0.1:8765"


def _api(method: str, path: str, **kwargs):
    try:
        resp = getattr(requests, method)(f"{API_BASE}{path}", timeout=10, **kwargs)
        resp.raise_for_status()
        return resp
    except requests.ConnectionError:
        click.echo(click.style("✗ MemoryOS server is not running. Run: memoryos start", fg="red"))
        sys.exit(1)


@click.group()
@click.version_option("1.0.0", prog_name="memoryos")
def cli():
    """MemoryOS — Your AI finally remembers you."""


@cli.command()
@click.option("--host", default="127.0.0.1", help="Bind host")
@click.option("--port", default=8765, help="API port")
@click.option("--dashboard-port", default=3000, help="Dashboard port")
@click.option("--no-browser", is_flag=True, help="Skip opening browser")
def start(host, port, dashboard_port, no_browser):
    """Start the MemoryOS local server."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    click.echo(click.style("🧠 Starting MemoryOS...", fg="cyan", bold=True))

    try:
        proc = subprocess.Popen(
            [
                sys.executable, "-m", "uvicorn",
                "app.main:app",
                "--host", host,
                "--port", str(port),
                "--reload" if os.environ.get("DEBUG") else "",
            ],
            cwd=Path(__file__).resolve().parents[1],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        PID_FILE.write_text(str(proc.pid))
        click.echo(click.style(f"✓ Server running at http://{host}:{port}", fg="green"))
        if not no_browser:
            webbrowser.open(f"http://localhost:{dashboard_port}")
        click.echo(click.style(
            "\n📦 Install the browser extension to start capturing AI conversations.",
            fg="yellow",
        ))
        click.echo("Press Ctrl+C to stop.")
        proc.wait()
    except KeyboardInterrupt:
        click.echo("\nStopping...")
        proc.terminate()
        PID_FILE.unlink(missing_ok=True)


@cli.command()
def stop():
    """Stop the MemoryOS server."""
    if not PID_FILE.exists():
        click.echo("Server is not running.")
        return
    pid = int(PID_FILE.read_text())
    try:
        os.kill(pid, signal.SIGTERM)
        PID_FILE.unlink(missing_ok=True)
        click.echo(click.style("✓ MemoryOS stopped.", fg="green"))
    except ProcessLookupError:
        click.echo("Server was not running.")
        PID_FILE.unlink(missing_ok=True)


@cli.command()
@click.argument("query")
@click.option("--limit", "-n", default=10, help="Number of results")
@click.option("--source", help="Filter by source (chatgpt, claude, etc.)")
def search(query, limit, source):
    """Search your memories semantically."""
    params = {"q": query, "limit": limit}
    if source:
        params["source"] = source
    results = _api("get", "/api/v1/search", params=params).json()
    if not results:
        click.echo("No memories found.")
        return
    for i, item in enumerate(results, 1):
        m = item["memory"]
        score = item["score"]
        text = m.get("summary") or m["content"][:100]
        click.echo(click.style(f"{i}. [{m['source']}] ", fg="cyan") + text)
        click.echo(click.style(f"   Score: {score:.2f} | {m['created_at'][:10]}", fg="bright_black"))


@cli.command()
@click.argument("content")
@click.option("--tags", "-t", default="", help="Comma-separated tags")
def add(content, tags):
    """Add a memory manually."""
    payload = {
        "content": content,
        "source": "cli",
        "tags": [t.strip() for t in tags.split(",") if t.strip()],
    }
    result = _api("post", "/api/v1/memories", json=payload).json()
    click.echo(click.style(f"✓ Memory saved: {result['id']}", fg="green"))


@cli.command()
@click.argument("memory_id")
def forget(memory_id):
    """Forget (soft-delete) a memory by ID."""
    _api("delete", f"/api/v1/memories/{memory_id}")
    click.echo(click.style(f"✓ Memory {memory_id} forgotten.", fg="yellow"))


@cli.command()
def stats():
    """Show memory statistics."""
    data = _api("get", "/api/v1/stats").json()
    click.echo(click.style("\n🧠 MemoryOS Stats\n", fg="cyan", bold=True))
    click.echo(f"  Total memories : {data.get('total_memories', 0)}")
    click.echo(f"  Pinned         : {data.get('pinned_memories', 0)}")
    click.echo(f"  Storage        : {data.get('storage_mb', 0)} MB")
    by_source = data.get("by_source", {})
    if by_source:
        click.echo("\n  By source:")
        for src, count in by_source.items():
            click.echo(f"    {src}: {count}")


@cli.command()
@click.option("--format", "fmt", default="markdown", type=click.Choice(["json", "markdown", "csv"]), help="Export format")
@click.option("--output", "-o", default="memories-export", help="Output file path (without extension)")
@click.option("--source", help="Filter by source")
def export(fmt, output, source):
    """Export all memories to a file."""
    params = {"format": fmt}
    if source:
        params["source"] = source
    resp = _api("get", "/api/v1/export", params=params)
    ext = {"json": ".json", "markdown": ".md", "csv": ".csv"}[fmt]
    out_path = Path(output).with_suffix(ext)
    out_path.write_bytes(resp.content)
    click.echo(click.style(f"✓ Exported to {out_path}", fg="green"))


@cli.command()
@click.argument("query")
@click.option("--max-tokens", default=2000)
def ask(query, max_tokens):
    """Get context from your memories for a query."""
    result = _api("get", "/api/v1/search/context", params={"q": query, "max_tokens": max_tokens}).json()
    context = result.get("context", "")
    if not context:
        click.echo("No relevant memories found.")
        return
    click.echo(click.style("\n📋 Relevant context from your memories:\n", fg="cyan", bold=True))
    click.echo(context)
    click.echo(click.style("\n💡 Paste the above into your AI conversation as context.", fg="yellow"))


if __name__ == "__main__":
    cli()
