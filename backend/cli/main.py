"""MemoryOS CLI — `memoryos` command."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

import click
import httpx

API_BASE = os.environ.get("MEMORYOS_API", "http://127.0.0.1:8765")


def _api(method: str, path: str, **kwargs) -> dict:
    url = f"{API_BASE}{path}"
    try:
        resp = httpx.request(method, url, timeout=30, **kwargs)
        resp.raise_for_status()
        return resp.json()
    except httpx.ConnectError:
        click.echo("❌ Cannot connect to MemoryOS server. Run: memoryos start", err=True)
        sys.exit(1)
    except httpx.HTTPStatusError as e:
        click.echo(f"❌ API error {e.response.status_code}: {e.response.text}", err=True)
        sys.exit(1)


@click.group()
@click.version_option("1.0.0", prog_name="memoryos")
def cli():
    """\U0001f9e0 MemoryOS — Your AI finally remembers you."""


@cli.command()
@click.option("--port", default=8765, help="API server port")
@click.option("--dashboard", is_flag=True, default=True, help="Also start dashboard")
def start(port: int, dashboard: bool):
    """Start the MemoryOS local server."""
    click.echo("🧠 Starting MemoryOS...")
    env = os.environ.copy()
    env["PORT"] = str(port)
    cmd = [
        sys.executable, "-m", "uvicorn",
        "app.main:app",
        "--host", "127.0.0.1",
        "--port", str(port),
        "--reload",
    ]
    backend_dir = Path(__file__).parent.parent
    click.echo(f"✅ API running at http://127.0.0.1:{port}")
    click.echo("📚 Dashboard: http://localhost:3000")
    click.echo("Press Ctrl+C to stop.")
    subprocess.run(cmd, cwd=str(backend_dir), env=env)


@cli.command()
def stop():
    """Stop the MemoryOS server (kills uvicorn process)."""
    subprocess.run(["pkill", "-f", "uvicorn app.main:app"], check=False)
    click.echo("✅ MemoryOS stopped.")


@cli.command()
@click.argument("query")
@click.option("--limit", "-n", default=5, help="Number of results")
def search(query: str, limit: int):
    """Semantic search across your memories."""
    results = _api("GET", f"/api/v1/search?q={query}&limit={limit}")
    if not results:
        click.echo("No results found.")
        return
    for i, item in enumerate(results, 1):
        m = item["memory"]
        score = item["score"]
        click.echo(f"\n[{i}] Score: {score:.3f} | Source: {m['source']} | {m['created_at'][:10]}")
        click.echo(f"    {m['content'][:200]}")
        if m.get("summary"):
            click.echo(f"    📝 {m['summary']}")


@cli.command()
@click.argument("content")
@click.option("--source", "-s", default="cli")
@click.option("--tags", "-t", multiple=True)
def add(content: str, source: str, tags: tuple):
    """Add a memory manually."""
    payload = {"content": content, "source": source, "tags": list(tags)}
    result = _api("POST", "/api/v1/memories", json=payload)
    click.echo(f"✅ Memory saved: {result['id']}")


@cli.command()
@click.argument("memory_id")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation")
def forget(memory_id: str, yes: bool):
    """Soft-delete a memory by ID."""
    if not yes:
        click.confirm(f"Forget memory {memory_id}?", abort=True)
    _api("DELETE", f"/api/v1/memories/{memory_id}")
    click.echo("✅ Memory forgotten.")


@cli.command()
def stats():
    """Show memory statistics."""
    data = _api("GET", "/api/v1/stats")
    click.echo("\n🧠 MemoryOS Stats")
    click.echo(f"  Total memories  : {data['total_memories']}")
    click.echo(f"  Total sessions  : {data['total_sessions']}")
    click.echo(f"  Total tags      : {data['total_tags']}")
    click.echo(f"  Pinned          : {data['pinned_memories']}")
    click.echo(f"  DB size         : {data['db_size_mb']} MB")


@cli.command()
@click.option("--format", "-f", type=click.Choice(["json", "markdown", "csv"]), default="markdown")
@click.option("--output", "-o", default="memoryos-export.md", help="Output file path")
def export(format: str, output: str):
    """Export all memories to file."""
    try:
        resp = httpx.post(f"{API_BASE}/api/v1/export?format={format}", timeout=60)
        resp.raise_for_status()
        Path(output).write_bytes(resp.content)
        click.echo(f"✅ Exported to {output}")
    except httpx.ConnectError:
        click.echo("❌ Cannot connect to MemoryOS server.", err=True)


@cli.command(name="import")
@click.argument("file", type=click.Path(exists=True))
def import_memories(file: str):
    """Import memories from a JSON export file."""
    data = json.loads(Path(file).read_text())
    result = _api("POST", "/api/v1/export/import", json=data)
    click.echo(f"✅ Imported {result['imported']} memories.")


@cli.command()
@click.argument("query")
@click.option("--max-tokens", default=2000)
def ask(query: str, max_tokens: int):
    """Get prompt-ready context from your memories."""
    result = _api("GET", f"/api/v1/search/context?q={query}&max_tokens={max_tokens}")
    click.echo("\n🧠 Relevant memory context:\n")
    click.echo(result.get("context", "No relevant memories found."))


def main():
    cli()


if __name__ == "__main__":
    main()
