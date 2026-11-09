from __future__ import annotations

import asyncio
import json
import sys
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from backend.sdk import polyglot

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

cli_app = typer.Typer(help="Polyglot Riff Atelier — Neo4j + PostgreSQL Bridge & Regional Converse CLI")
console = Console()


def _run(coro):
    async def _wrapped():
        try:
            return await coro
        finally:
            await polyglot.close()

    return asyncio.run(_wrapped())


@cli_app.command("status")
def cmd_status() -> None:
    """Check health and counts across PostgreSQL (pgvector), Neo4j (+APOC), and Ollama."""
    res = _run(polyglot.status())
    console.print_json(json.dumps(res, ensure_ascii=False, default=str))


@cli_app.command("seed")
def cmd_seed(no_embed: bool = typer.Option(False, "--no-embed", help="Skip bge-m3 embedding backfill")) -> None:
    """Idempotently initialize schemas, seed all 5 Formal<->Regional language pairs, embed with bge-m3, and sync Neo4j + db/*.db.json."""
    res = _run(polyglot.seed(compute_embeddings=not no_embed))
    console.print(Panel.fit("[bold green]✓ Seed + Embedding + Neo4j Sync Complete[/bold green]"))
    console.print_json(json.dumps(res, ensure_ascii=False, default=str))


@cli_app.command("sync")
def cmd_sync(
    force: bool = typer.Option(False, "--force", help="Force full resync of all rows"),
    prune_orphans: bool = typer.Option(False, "--prune-orphans", help="Delete orphan Neo4j nodes/edges absent from Postgres"),
) -> None:
    """Replay pending PostgreSQL outbox changes to Neo4j and refresh atomic db/*.db.json snapshots."""
    res = _run(polyglot.sync(force_all=force, prune_orphans=prune_orphans))
    console.print_json(json.dumps(res, ensure_ascii=False, default=str))


@cli_app.command("audit")
def cmd_audit() -> None:
    """Run end-to-end 4-layer data integrity audit across PostgreSQL, Neo4j, bge-m3 vectors, and db/*.db.json shards."""
    res = _run(polyglot.audit())
    console.print_json(json.dumps(res, ensure_ascii=False, default=str))
    if not res.get("ok"):
        raise typer.Exit(code=1)


@cli_app.command("backup")
def cmd_backup(
    keep_last: int = typer.Option(10, "--keep-last", help="Number of timestamped snapshots to retain in backups/"),
) -> None:
    """Create an atomic, SHA-256-checksummed PostgreSQL JSON + Neo4j Cypher snapshot in backups/."""
    res = _run(polyglot.backup(keep_last=keep_last))
    console.print(Panel.fit(f"[bold green]✓ Backup Snapshot Saved:[/bold green] {res['snapshot_dir']}"))
    console.print_json(json.dumps(res, ensure_ascii=False, default=str))


@cli_app.command("bridge")
def cmd_bridge(
    from_reg: str = typer.Option("AT_VIE", "--from", help="Source register, e.g. AT_VIE or CZ_STD"),
    to_reg: str = typer.Option("CZ_OVA", "--to", help="Target register, e.g. CZ_OVA or RU_ALA"),
    stage: str = typer.Option("CHAMELEON", "--stage", help="Starting 4-C stage"),
) -> None:
    """Find optimal multi-hop Neo4j (:PIVOTS_VIA) + pgvector bridge paths between registers."""
    res = _run(polyglot.bridge(from_reg, to_reg, stage=stage))
    console.print_json(json.dumps(res, ensure_ascii=False, default=str))


@cli_app.command("scaffold")
def cmd_scaffold(
    card: Optional[str] = typer.Option(None, "--card", help="Card UID, e.g. CZ_OVA_COUNT"),
    text: Optional[str] = typer.Option(None, "--text", help="Free text to scaffold"),
    reg: str = typer.Option("CZ_OVA", "--reg", help="Target regional register"),
    anchors: str = typer.Option("DE,RU,EN", "--anchors", help="Comma-separated bridge languages"),
) -> None:
    """Resolve 3-layer bridge scaffolding (cognates/calques/false-friends, :PIVOTS_VIA, and :SHARES_VIBE_WITH + pgvector)."""
    anchor_list = [a.strip().upper() for a in anchors.split(",") if a.strip()]
    res = _run(polyglot.scaffold(card_uid=card, text=text, target_register=reg, anchor_langs=anchor_list))
    console.print_json(json.dumps(res, ensure_ascii=False, default=str))


@cli_app.command("switcher")
def cmd_switcher(lang: str = typer.Option("cs", "--lang", help="Language code: cs, de, ru, en, es")) -> None:
    """Display the Formal Boardroom -> Register-Drop Bridge -> Regional Insider sequence for any language."""
    res = _run(polyglot.switcher(lang_code=lang))
    table = Table(title=f"Register Switcher Flow — {res['language']['flag']} {res['language']['name']} ({lang})")
    table.add_column("Step / Stage", style="cyan")
    table.add_column("Register", style="magenta")
    table.add_column("Spoken Riff", style="white")
    table.add_column("Vocal Cue", style="green")
    for item in res["sequence"]:
        table.add_row(item["stage"], item["reg"], item["text"], item["delivery"])
    console.print(table)


@cli_app.command("converse")
def cmd_converse(
    reg: str = typer.Option("CZ_OVA", "--reg", help="Target register ID"),
    arena: str = typer.Option("polo", "--arena", help="Arena: terrace, spark, adventure, runway, hochkultur, polo, wien, b2b"),
    stage: str = typer.Option("COUNTERACT", "--stage", help="4-C stage"),
    lens: str = typer.Option("FERGUSON", "--lens", help="Lens: DEADPAN, SABOTEUR, RACONTEUR, FERGUSON, ONEAL, WILLIAMS"),
) -> None:
    """Resolve regional converse style by (register x arena x stage x comic/salon lens) with bridge scaffolding."""
    res = _run(polyglot.converse(register=reg, arena=arena, stage=stage, lens=lens))
    console.print_json(json.dumps(res, ensure_ascii=False, default=str))


@cli_app.command("shards")
def cmd_shards() -> None:
    """Export offline db/*.db.json shards directly from the canonical seed corpus (no running DB required)."""
    from backend.services.sync_service import sync_service

    written = sync_service.export_offline_db_json_from_seed()
    console.print_json(json.dumps({"ok": True, "written_shards": written}, ensure_ascii=False))


@cli_app.command("stylize")
def cmd_stylize(
    thought: str = typer.Argument(..., help="Raw thought in EN/DE/RU to transform into target regional speech"),
    reg: str = typer.Option("CZ_OVA", "--reg", help="Target register ID"),
    arena: str = typer.Option("terrace", "--arena", help="Social arena"),
    stage: str = typer.Option("COUNTERACT", "--stage", help="4-C stage"),
    lens: str = typer.Option("FERGUSON", "--lens", help="Delivery / comic lens"),
    fast: bool = typer.Option(False, "--fast", help="Use gemma3:4b fast mode instead of gemma4:12b"),
    commit: bool = typer.Option(False, "--commit", help="Commit directly into Postgres + Neo4j instead of staging"),
) -> None:
    """Transform a raw thought into authentic regional speech via local Ollama + strict relation & false-friend guardrails."""
    res = _run(
        polyglot.stylize(
            thought,
            target_register=reg,
            arena=arena,
            stage=stage,
            lens=lens,
            fast_mode=fast,
            commit=commit,
        )
    )
    console.print_json(json.dumps(res, ensure_ascii=False, default=str))


@cli_app.command("grade")
def cmd_grade(edge_id: str, score: int) -> None:
    """Record an FSRS practice score (1-5) for a transition edge and sync to Neo4j."""
    res = _run(polyglot.grade(edge_id=edge_id, score=score))
    console.print_json(json.dumps(res, ensure_ascii=False, default=str))


if __name__ == "__main__":
    cli_app()
