# Polyglot Interpersonal Riff Studio & Neo4j SRS Engine (`v3.4.0`)

**Live On-the-Go Web App (GitHub Pages):** [https://hotpopize.github.io/polyglot-riff-studio/](https://hotpopize.github.io/polyglot-riff-studio/)  
**Architecture & Lineage Map:** [CODEBASE_LINEAGE_AND_MAP.md](CODEBASE_LINEAGE_AND_MAP.md) • [architecture_and_flow_notes.md](architecture_and_flow_notes.md) • [quick_launch_prompts_and_commands.md](quick_launch_prompts_and_commands.md)

---

## Quick Start

### 1. On-the-Go / Mobile & Desktop Browser (Zero Setup)
Open **[https://hotpopize.github.io/polyglot-riff-studio/](https://hotpopize.github.io/polyglot-riff-studio/)** on any phone, tablet, or laptop.
* Hydrates in `< 30ms` from the 6 deterministic [`db/*.db.json`](db/) shards (`196` 4-C cards, `8` social arenas, `35` IB past-paper & regional `:Vocab` anchors, `6` regional `:Song` anthems).
* Works 100% offline via the Service Worker ([`sw.js`](sw.js)) and queues FSRS drill grades in `localStorage` until reconnected to your local stack.

### 2. Full Local 4-Layer Stack (PostgreSQL 17 `pgvector` + Neo4j 5.26 `APOC` + FastAPI + Ollama)
```powershell
.\start_polyglot_stack.ps1
```
* **Local Suite Hub**: `http://127.0.0.1:8765/index.html`
* **Wi-Fi LAN Mobile URL**: Printed in terminal & shown in the **🌐 Mobile / Sync** modal inside `index.html`.
* **Neo4j Browser**: `http://127.0.0.1:7474` (`neo4j` / `polyglot_atelier_dev`)

### 3. Verify 4-Layer Data Parity & Publish Updates to GitHub Pages
```powershell
.\.venv\Scripts\python.exe -m backend.cli audit
.\publish_github_pages.ps1
```

---

## Where Everything Lives
See **[CODEBASE_LINEAGE_AND_MAP.md](CODEBASE_LINEAGE_AND_MAP.md)** for the complete version lineage (`v1.0` → `v3.4`), Single Source of Truth (SSOT) editing rules, and file-by-file directory reference.
