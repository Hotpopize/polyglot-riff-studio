This is a single self-contained fix; keep it small and focused. Use a small, focused team (one implementer, then repeated adversarial review) for the core area and headers with others understanding the work and connectors. Implement the interactive 9×9 Lotus grid in Tab 6 of the Polyglot Riff Atelier web suite, styled after the AbrisOps 9×9 example grid while matching the color theme of the web app, aimed at becoming a proficient sales polyglot while having fun by synthesizing personas, languages, themes, phrases, bridges, graph relations, and builds around Polyglot Atelier Salesact.

Working directory: c:\Assets\PolyglotSales
Integrity mode: development

Reference material:
- Reference 9×9 Lotus layout screenshot: `C:/Users/iamab/.gemini/antigravity/brain/e826fe70-7f60-4707-9cf0-5c403793a684/.user_uploaded/media_1793797263908_85c6daff.jpg`
- Polyglot Atelier WBS and 81-cell matrix specification: `c:\Assets\PolyglotSales\checkpoint_and_wetwork_wbs_9x9.md`
- Target single-file web application: `c:\Assets\PolyglotSales\polyglot_riff_studio_v3_1_atelier_edition.html`

## Requirements

### R1. Tab 6 ("6. Checkpoint • Wetwork • 9×9") Integration
Add Tab 6 ("6. Checkpoint • Wetwork • 9×9") to the top navigation bar and view switcher of `polyglot_riff_studio_v3_1_atelier_edition.html`. Integrate the complete 9×9 Lotus grid view alongside the Checkpoint and Wetwork WBS documentation, fully connected to the existing view switching system.

### R2. 9×9 Lotus Layout Topology & Styling (Polyglot Atelier Salesact)
Construct the 9×9 grid strictly following the true Lotus / Mandalart topology from the AbrisOps reference while matching the color theme of `polyglot_riff_studio_v3_1_atelier_edition.html`:
- **Center 3×3 Block Topology**: The absolute center core cell at `[5,5]` is named **`Polyglot Atelier Salesact`**. The eight cells surrounding it in the center 3×3 block explicitly name the eight themes (`1 · ...` through `8 · ...`) around `Polyglot Atelier Salesact`.
- **Outer 3×3 Blocks Topology**: Each of the eight themes from the center block is concurrently the center header cell of its own outer 3×3 block (cells `[2,2]`, `[2,5]`, `[2,8]`, `[5,2]`, `[5,8]`, `[8,2]`, `[8,5]`, and `[8,8]`), surrounded by its eight specific tactics, idioms, bridges, graph relations, or builds.
- **Color Theme Integration**: Match the web app's dark slate palette (`#090d16` canvas, `slate-950`/`slate-900` card fills, `slate-800`/`slate-700` crisp hairline borders, and `slate-600`/`indigo-500` prominent thick border dividers between the nine 3×3 blocks). Theme header cells and the center core cell use the app's accent palette (`indigo`, `amber`, `emerald`, `rose`), with `Polyglot Atelier Salesact` styled as a high-contrast focal centerpiece.
- **Metadata Sections**:
  - Top header displays title, subtitle, and Lotus layout description: *"Lotus layout for Polyglot Atelier Salesact: the centre block names eight themes around Polyglot Atelier Salesact; each theme is the centre of its own block with eight automations/tactics..."*
  - Bottom footer displays the `Key:` (eight themes 1–8) and `Rules every cell obeys:` blocks.
- **Reference Grid Toggle**: Include a toggle control allowing the user to switch the view between the Polyglot Atelier Salesact 9×9 matrix and the original AbrisOps reference grid.

### R3. Data Synthesis & Cell Interaction
Populate the 81 cells across all nine blocks from `checkpoint_and_wetwork_wbs_9x9.md`:
- Themes 1–4: Regional language anchors (`1 · CZ_OVA Czech-from-Zero`, `2 · AT_VIE Wiener Schmäh`, `3 · RU_ALA Almaty Insider`, `4 · EN_YYC & ES_SOT Foothills & Sotogrande`).
- Theme 5: 4-C flow and objection interrupts (`5 · 4-C & :COUNTERS_STATE`).
- Theme 6: Persona and comic styles (`6 · 6 Persona Lenses`).
- Theme 7: High-society salons and field wetwork (`7 · Salons & Station Wien`).
- Theme 8: Federated architecture and AI (`8 · Multi-DB & Ollama/Webhooks`).
- Center `[5,5]`: `Polyglot Atelier Salesact`.
Clicking any cell opens an inspection modal or detail panel showing full cognate notes, persona posture, cross-language bridges (`:PIVOTS_VIA`, `:SHARES_VIBE_WITH`), and direct navigation shortcuts to relevant studio tabs.

### R4. Synchronization with Markdown Reference
Update `checkpoint_and_wetwork_wbs_9x9.md` Section 3.2 so that its 9×9 Harada / Mandalart table, center block, and core cell naming strictly align with `Polyglot Atelier Salesact` and the Lotus matrix topology.

## Acceptance Criteria

### Topology & Structural Integrity
- [ ] Tab 6 ("6. Checkpoint • Wetwork • 9×9") is present in the navigation header and active when selected via `switchMode('wetwork')` or equivalent.
- [ ] The 9×9 table renders 81 distinct cells arranged in nine 3×3 blocks, with prominent thicker border dividers separating the blocks.
- [ ] Center cell `[5,5]` is named `Polyglot Atelier Salesact`. The surrounding eight cells of the center 3×3 block display the eight themes (`1 · ...` through `8 · ...`).
- [ ] Each of the eight outer 3×3 blocks has its corresponding theme (`1 · ...` through `8 · ...`) at its center, surrounded by its eight specific tactics/phrases/bridges.
- [ ] Top section contains title, subtitle, and Lotus layout explanation; bottom section contains the Key (themes 1–8) and Rules blocks.
- [ ] A toggle control switches the display between the Polyglot Atelier Salesact 9×9 grid and the AbrisOps reference grid.

### Visual Layout & Color Scheme
- [ ] Cell backgrounds, borders, and typography match the existing web app color scheme (`#090d16` / `slate-950` / `slate-900` / `slate-800`), with the 8 outer pillar centers and the center core cell utilizing app accents (`indigo`, `amber`, `emerald`, `rose`) to create clear visual hierarchy without clashing with the existing tabs.

### Interactivity & Synchronization
- [ ] Clicking on cells inspects cell metadata (e.g. cognate notes, persona details, or bridge relations).
- [ ] No regression occurs in existing tabs (Tab 1 4-C Studio, Tab 2 Neo4j Force-Graph, Tab 3 Salons, Tab 4 Blitz, Tab 5 Builder).
- [ ] `checkpoint_and_wetwork_wbs_9x9.md` is synchronized to reflect `Polyglot Atelier Salesact` and the Lotus matrix topology.

### Automated Verification
- [ ] A verification script (e.g., Node.js / Puppeteer or DOM inspection script) runs against `polyglot_riff_studio_v3_1_atelier_edition.html`, confirming that all 81 cells are rendered with correct Lotus topology (cell `[5,5]` = `Polyglot Atelier Salesact`, center block holds themes 1–8, outer blocks hold themes 1–8 at their centers), block boundaries have distinct border styling matching the app palette, and tab switching succeeds with zero JavaScript console errors.
