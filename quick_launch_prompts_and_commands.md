# Polyglot Riff Studio — Quick-Launch Prompts & Commands

Use these copy-paste prompts and one-liners to spin up pre-call sparring drills, generate new 4-C decks for **Atelier v3.1**, or expand the **Czech B2B Register Switcher**.

---

## 1. One-Click & Terminal Quick Launchers

### Windows Explorer (Zero-Terminal)
- Double-click **`launch_studio.cmd`** to boot the full **Neo4j 5 + PostgreSQL 17 (`pgvector`) + FastAPI (`:8765`) + Polyglot Suite Hub** stack (automatically falls back to `index.html` if offline).

### PowerShell Full-Stack & Backend CLI One-Liners
```powershell
# 1. One-Click Full Stack (Docker Neo4j + pgvector:5433 + Corpus Seed + FastAPI :8765 + Browser)
cd C:\Assets\PolyglotSales; .\start_polyglot_stack.ps1

# 2. Check Live Backend Health (PostgreSQL:5433, Neo4j:7687, Ollama bge-m3 & gemma4:12b)
cd C:\Assets\PolyglotSales; .\.venv\Scripts\python.exe -m backend.cli status

# 3. Run / Re-Run Corpus Migration, bge-m3 Embeddings & Neo4j + db/*.db.json Sync
cd C:\Assets\PolyglotSales; .\.venv\Scripts\python.exe -m backend.cli seed

# 4. Query 3-Layer Bridge Scaffolds (DE/RU/EN -> CZ_OVA + FalseFriend Shields + pgvector)
cd C:\Assets\PolyglotSales; .\.venv\Scripts\python.exe -m backend.cli scaffold --text "Let's focus on real traction without circus" --reg CZ_OVA

# 5. Query Multi-Hop Neo4j :PIVOTS_VIA Bridge Paths
cd C:\Assets\PolyglotSales; .\.venv\Scripts\python.exe -m backend.cli bridge --from AT_VIE --to RU_ALA --stage CHAMELEON

# 6. Resolve Regional Converse Style Coordinates (Register x Arena x 4-C Stage x Comic Lens)
cd C:\Assets\PolyglotSales; .\.venv\Scripts\python.exe -m backend.cli converse --reg CZ_OVA --arena polo --stage COUNTERACT --lens FERGUSON

# 7. Live Thought Stylizer via Ollama (gemma4:12b default, gemma3:4b fast mode)
cd C:\Assets\PolyglotSales; .\.venv\Scripts\python.exe -m backend.cli stylize "Cut the slide-deck theatre and ship clean steel" --reg CZ_OVA --lens FERGUSON --fast

# 8. Inspect 5-Language Formal <-> Bridge <-> Regional Switcher Deck
cd C:\Assets\PolyglotSales; .\.venv\Scripts\python.exe -m backend.cli switcher --lang de

# 9. Open Live Suite Hub (:8765) or Neo4j Browser (:7474, auth: neo4j / polyglot_atelier_dev)
Start-Process "http://127.0.0.1:8765/index.html"
Start-Process "http://127.0.0.1:7474"
```

### Local MCP Server Configuration (`polyglot-atelier`)
Add to your MCP client config to give AI sparring agents live access to Neo4j + `pgvector` bridges, regional converse styles, and FSRS grading:
```json
{
  "mcpServers": {
    "polyglot-atelier": {
      "command": "C:\\Assets\\PolyglotSales\\.venv\\Scripts\\python.exe",
      "args": ["-m", "backend.mcp_server"],
      "cwd": "C:\\Assets\\PolyglotSales"
    }
  }
}
```

### Standalone Offline HTML Launchers (`file://` Fallback)
```powershell
# Launch Atelier v3.1 (Full Neo4j SRS Engine + 9x9 Lotus) directly
cd C:\Assets\PolyglotSales; Start-Process .\polyglot_riff_studio_v3_1_atelier_edition.html

# Launch 5-Language Formal <-> Regional Switcher directly
cd C:\Assets\PolyglotSales; Start-Process .\czech_register_switcher_widget.html

# Launch Neo4j SRS Heatmap v3.0 or Zero-Corporate Lounge v1.0 directly
cd C:\Assets\PolyglotSales; Start-Process .\polyglot_riff_studio_v3_0_neo4j_srs_heatmap.html
cd C:\Assets\PolyglotSales; Start-Process .\polyglot_riff_studio_v1_zero_corporate.html
```

### Command Prompt (`cmd.exe`) One-Liners (Run from Anywhere)
```cmd
cd /d C:\Assets\PolyglotSales && launch_studio.cmd
```

---

## 2. Quick-Launch Prompts for Live Pre-Call Warmups & Deck Expansion

### Prompt A: 3-Minute Pre-Call B2B Sparring (Czech C-Suite → Dev Trench)
> **Copy/Paste:**
> "Run a 3-minute Czech B2B pre-call warmup with me using `@czech_register_switcher_widget.html` and `@neo4j_seed_objection_states_and_false_friends.cypher`.
> 1. Give me an executive C-Suite objection in *Spisovná čeština* (`Vykání`), addressing me in the 5th-case Vocative.
> 2. Wait for my `[COMPLIMENT]` + `[CHAMELEON]` response.
> 3. Then bring in the Lead Engineer from Ostrava who is skeptical of manual pipeline overhead (`MANUAL_GRIND`), so I have to execute the `BR_CZ_STD_TO_OVA` register-drop bridge and land a `[COUNTERACT]` using Silesian/industrial loans (`fachat`, `šichta`, `fajront`, `bo`) without triggering any Russian false friends."

---

### Prompt B: Generate a New 4-C Industry Scenario (JSON & Workbench Ready)
> **Copy/Paste:**
> "Generate a new 4-C conversational riff chain (`1. COMPLIMENT`, `2. CHAMELEON`, `3. COUNTERACT`, `4. CURIOSITY`) for **`[TARGET PERSONA: CZ_OVA | AT_VIE | RU_ALA | EN_YYC | ES_SOT]`** tailored to **`[INDUSTRY / SCENARIO, e.g., Cloud Migration / FinTech Latency / Fashion Week Backstage]`**.
> Include:
> - 2 dashed `<span class="slang-token" data-term="...">` regional idioms with their etymological root, acoustic delivery cue (pitch drop / vowel length), and a `:SHARES_VIBE_WITH` cousin from another persona in `@polyglot_riff_studio_v3_1_atelier_edition.html`.
> - A `:COUNTERS_STATE` objection mapping (`MANUAL_GRIND`, `CORPORATE_SHIELD`, `OVERTHINKING`, or `PLAYING_IT_SAFE`).
> - Output both the Workbench fields and the ready-to-wire code for `@polyglot_riff_studio_v3_1_atelier_edition.html`."

---

### Prompt C: Cross-Language Chameleon Bridge Generator (`:PIVOTS_VIA`)
> **Copy/Paste:**
> "Create 3 mid-sentence code-switching `:Bridge` nodes (`:PIVOTS_VIA`) transitioning from **`[SOURCE LANG, e.g., AT_VIE]`** at stage `[2. CHAMELEON]` into **`[TARGET LANG, e.g., CZ_OVA or RU_ALA]`** at stage `[3. COUNTERACT]`.
> Ensure the switch obeys Myers-Scotton's Matrix Language Frame constraints (switching at a natural discourse particle or clause boundary), and include the exact vocal inflection cue."

---

### Prompt D: 60-Second Trilingual Interference Blitz (`CZ` / `RU` / `DE`)
> **Copy/Paste:**
> "Quiz me on 5 rapid-fire B2B sentences where a Russian speaker would accidentally use a Slavic false friend in Czech (e.g., *úžasný, čerstvý, nápad, vyprodat, pozor, hodina, zapomenout, přesný, směšný*). Give me the English/Russian thought, and make me translate it into natural Czech using the correct German structural calque (e.g., *zaměřit se na*, *spoléhat se na*, *dávat pozor na*) and 5th-case Vocative."

---

### Prompt E: Station Wien / Runway 27-Minute Immersion Drill
> **Copy/Paste:**
> "Launch a 10-minute **Station Wien** trilingual intercept drill based on `@czech_from_zero_runway_and_station_wien.md`. Put me at the corner table in Vienna: alternate lines between Viennese German (`AT_VIE`), Czech (`CZ_OVA`/`CZ_STD`), and Russian (`RU_ALA`) with zero English explanations, testing whether I can shadow and pivot personas without translating in my head."

