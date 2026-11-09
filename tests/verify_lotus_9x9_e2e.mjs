import assert from 'node:assert/strict';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { validateCandidateGraphCommit } from '../db/graph_relation_validator.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');

const CHROME_CANDIDATES = [
  'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
  'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
];

function startStaticServer(rootDir) {
  const mime = {
    '.html': 'text/html; charset=utf-8',
    '.js': 'application/javascript; charset=utf-8',
    '.json': 'application/json; charset=utf-8',
    '.md': 'text/markdown; charset=utf-8',
    '.css': 'text/css; charset=utf-8'
  };
  return new Promise((resolve) => {
    const server = http.createServer((req, res) => {
      const reqPath = decodeURIComponent((req.url || '/').split('?')[0]);
      const safeRel = reqPath === '/' ? 'index.html' : reqPath.replace(/^\/+/, '');
      const fullPath = path.join(rootDir, safeRel);
      if (!fullPath.startsWith(rootDir) || !fs.existsSync(fullPath) || fs.statSync(fullPath).isDirectory()) {
        res.writeHead(404);
        res.end('Not found');
        return;
      }
      const ext = path.extname(fullPath).toLowerCase();
      res.writeHead(200, { 'Content-Type': mime[ext] || 'application/octet-stream' });
      res.end(fs.readFileSync(fullPath));
    });
    server.listen(0, '127.0.0.1', () => {
      resolve({ server, port: server.address().port });
    });
  });
}

async function waitForJsonVersion(debugPort, timeoutMs = 10000) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    try {
      const r = await fetch(`http://127.0.0.1:${debugPort}/json/list`);
      if (r.ok) {
        const list = await r.json();
        const page = list.find(t => t.type === 'page' && t.webSocketDebuggerUrl);
        if (page) return page.webSocketDebuggerUrl;
      }
    } catch {}
    await new Promise(r => setTimeout(r, 150));
  }
  throw new Error('Timed out waiting for headless browser CDP endpoint');
}

class CdpSession {
  constructor(wsUrl) {
    this.wsUrl = wsUrl;
    this.id = 0;
    this.pending = new Map();
    this.consoleErrors = [];
    this.pageExceptions = [];
  }

  async connect() {
    this.ws = new WebSocket(this.wsUrl);
    await new Promise((resolve, reject) => {
      this.ws.addEventListener('open', resolve, { once: true });
      this.ws.addEventListener('error', reject, { once: true });
    });
    this.ws.addEventListener('message', (ev) => {
      const msg = JSON.parse(String(ev.data));
      if (msg.id && this.pending.has(msg.id)) {
        const { resolve, reject } = this.pending.get(msg.id);
        this.pending.delete(msg.id);
        if (msg.error) reject(new Error(msg.error.message));
        else resolve(msg.result);
      } else if (msg.method === 'Runtime.exceptionThrown') {
        this.pageExceptions.push(msg.params.exceptionDetails?.text || JSON.stringify(msg.params));
      } else if (msg.method === 'Runtime.consoleAPICalled' && msg.params.type === 'error') {
        const txt = (msg.params.args || []).map(a => a.value ?? a.description ?? '').join(' ');
        if (!txt.includes('favicon.ico')) {
          this.consoleErrors.push(txt);
        }
      }
    });
    await this.send('Page.enable');
    await this.send('Runtime.enable');
  }

  send(method, params = {}) {
    const id = ++this.id;
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }

  async eval(expression) {
    const res = await this.send('Runtime.evaluate', {
      expression,
      returnByValue: true,
      awaitPromise: true
    });
    if (res.exceptionDetails) {
      throw new Error(`Eval exception: ${res.exceptionDetails.text} ${res.exceptionDetails.exception?.description || ''}`);
    }
    return res.result.value;
  }

  close() {
    if (this.ws) this.ws.close();
  }
}

function stripMdCellFormatting(raw) {
  return raw
    .trim()
    .replace(/\*\*/g, '')
    .replace(/\*/g, '')
    .replace(/`/g, '')
    .replace(/\$R\(t\) \\ge 85\\%\$/g, 'R(t) ≥ 85%')
    .replace(/\s+/g, ' ')
    .trim();
}

async function main() {
  let passedChecks = 0;
  const check = (name, cond, detail = '') => {
    assert.ok(cond, `FAILED: ${name}${detail ? ' — ' + detail : ''}`);
    passedChecks++;
    console.log(`  [PASS] ${name}`);
  };

  console.log('=== 1. Validating Federated /db/*.db.json & Graph Relation Validator ===');
  const dbDir = path.join(ROOT_DIR, 'db');
  const dbFiles = ['cz_ova.db.json', 'at_vie.db.json', 'ru_ala.db.json', 'en_yyc.db.json', 'es_sot.db.json', 'polyglot_fabric.db.json'];
  for (const f of dbFiles) {
    const parsed = JSON.parse(fs.readFileSync(path.join(dbDir, f), 'utf8'));
    check(`DB shard ${f} parses cleanly`, typeof parsed === 'object' && parsed !== null);
  }
  const sampleVal = validateCandidateGraphCommit({
    card: { lang: 'CZ_OVA', stage: 'COUNTERACT', text: 'To musí <span class="slang-token" data-term="fachat">fachat</span>.' },
    idiom: { term: 'fachat' },
    edge: { weight: 0.85, stability: 10 },
    targetDb: 'CZ_OVA'
  });
  check('graph_relation_validator.js passes valid candidate', sampleVal.valid === true);
  const invalidVal = validateCandidateGraphCommit({
    card: { lang: 'CZ_OVA', stage: 'INVALID_STAGE', text: 'Missing token' },
    idiom: { term: 'fachat' },
    edge: { weight: 1.5 },
    targetDb: 'AT_VIE'
  });
  check('graph_relation_validator.js rejects invalid candidate across all rules', invalidVal.valid === false && invalidVal.checks.every(c => !c.passed));

  console.log('\n=== 2. Launching Headless Browser E2E Verification ===');
  const browserBin = CHROME_CANDIDATES.find(p => fs.existsSync(p));
  assert.ok(browserBin, 'No Chrome/Edge binary found for headless E2E');

  const { server, port } = await startStaticServer(ROOT_DIR);
  const debugPort = 9345 + Math.floor(Math.random() * 400);
  const userDataDir = path.join(ROOT_DIR, '.tmp_cdp_profile_' + Date.now());

  const targetUrl = `http://127.0.0.1:${port}/polyglot_riff_studio_v3_1_atelier_edition.html`;
  const proc = spawn(browserBin, [
    '--headless=new',
    '--disable-gpu',
    '--no-first-run',
    '--no-default-browser-check',
    '--window-size=1440,1200',
    `--user-data-dir=${userDataDir}`,
    `--remote-debugging-port=${debugPort}`,
    'about:blank'
  ], { stdio: 'ignore' });

  const waitForAppReady = async (session, timeoutMs = 10000) => {
    const deadline = Date.now() + timeoutMs;
    while (Date.now() < deadline) {
      try {
        const ready = await session.eval(
          `document.readyState === 'complete' && document.querySelectorAll('#lotus-9x9-table tr').length === 9 && document.querySelectorAll('#cards-container > div').length >= 4`
        );
        if (ready === true) return;
      } catch {
        // Ignore transient execution-context swaps while navigation commits
      }
      await new Promise(r => setTimeout(r, 100));
    }
    throw new Error('Timed out waiting for Polyglot Atelier DOM & Lotus 9x9 readiness');
  };

  let cdp;
  try {
    const wsUrl = await waitForJsonVersion(debugPort);
    cdp = new CdpSession(wsUrl);
    await cdp.connect();
    await cdp.send('Emulation.setDeviceMetricsOverride', {
      width: 1440,
      height: 1200,
      deviceScaleFactor: 1.5,
      mobile: false
    });
    await cdp.send('Page.navigate', { url: targetUrl });
    await waitForAppReady(cdp);

    // Check Tab 6 Nav Button
    const navBtnText = await cdp.eval(`document.getElementById('btn-mode-wetwork')?.textContent.trim()`);
    check('Tab 6 button exists in header with exact label', navBtnText === '6. Checkpoint • Wetwork • 9×9', navBtnText);

    // Verify all 6 tabs switch cleanly without regression
    const tabResults = await cdp.eval(`(() => {
      const modes = ['studio', 'graph', 'haute', 'shield', 'builder', 'wetwork'];
      const out = {};
      for (const m of modes) {
        switchMode(m);
        const visibleViews = modes.filter(x => !document.getElementById('view-' + x).classList.contains('hidden'));
        out[m] = {
          visibleViews,
          svgNodes: m === 'graph' ? document.querySelectorAll('#neo4j-svg circle').length : null,
          hauteCards: m === 'haute' ? document.querySelectorAll('#haute-cards-grid > div').length : null,
          comicTabs: m === 'haute' ? document.querySelectorAll('#comic-style-tabs > button').length : null,
          falseFriends: m === 'shield' ? document.querySelectorAll('#false-friend-tbody tr').length : null,
          dbPills: m === 'builder' ? document.querySelectorAll('#lang-db-pills > button').length : null
        };
      }
      return out;
    })()`);

    for (const m of ['studio', 'graph', 'haute', 'shield', 'builder', 'wetwork']) {
      check(`switchMode('${m}') isolates view-${m} cleanly`, tabResults[m].visibleViews.length === 1 && tabResults[m].visibleViews[0] === m);
    }
    check('Tab 2 (Force-Graph) renders D3 SVG nodes cleanly', tabResults.graph.svgNodes >= 25, `nodes=${tabResults.graph.svgNodes}`);
    check('Tab 3 (Salons) renders 6 Persona/Comic styles & 5 language cards', tabResults.haute.comicTabs === 6 && tabResults.haute.hauteCards === 5);
    check('Tab 4 (Blitz) renders all 9 False-Friend rows', tabResults.shield.falseFriends === 9);
    check('Tab 5 (Builder) renders all 6 DB partition pills', tabResults.builder.dbPills === 6);

    // Inspect Tab 6 Lotus 9x9 Topology in Polyglot Atelier Salesact mode
    const lotusAudit = await cdp.eval(`(() => {
      switchMode('wetwork');
      selectLotusCell(5, 5);
      const trs = Array.from(document.querySelectorAll('#lotus-9x9-table tbody tr'));
      const cells = Array.from(document.querySelectorAll('#lotus-9x9-table tbody td'));
      const pillRects = Array.from(document.querySelectorAll('#lotus-theme-pills button')).map(b => Math.round(b.getBoundingClientRect().top));
      const grid = trs.map(tr => Array.from(tr.querySelectorAll('td')).map(td => ({
        row: Number(td.dataset.row),
        col: Number(td.dataset.col),
        role: td.dataset.role,
        theme: Number(td.dataset.theme),
        className: td.className,
        text: td.textContent.trim(),
        childElemCount: td.querySelector('span')?.children.length || 0,
        borderRight: getComputedStyle(td).borderRightWidth,
        borderBottom: getComputedStyle(td).borderBottomWidth,
        fontWeight: getComputedStyle(td).fontWeight,
        bgImage: getComputedStyle(td).backgroundImage
      })));
      return {
        rowCount: trs.length,
        cellCount: cells.length,
        pillCount: pillRects.length,
        pillRowTops: Array.from(new Set(pillRects)),
        coreTwinLinkedCount: document.querySelectorAll('#lotus-9x9-table .lotus-cell-twin-linked').length,
        hasLegacyToggleDom: Boolean(document.querySelector('[id*="lotus-"][id*="toggle"], [onclick*="switchLotusDataset"]')),
        hasSwitchFn: typeof window.switchLotusDataset !== 'undefined',
        title: document.getElementById('lotus-title')?.textContent.trim(),
        subtitle: document.getElementById('lotus-subtitle')?.textContent.trim(),
        description: document.getElementById('lotus-description')?.textContent.trim(),
        keyText: document.getElementById('lotus-footer-key')?.textContent.trim(),
        rulesText: document.getElementById('lotus-footer-rules')?.textContent.trim(),
        domTextLower: document.documentElement.innerHTML.toLowerCase(),
        grid
      };
    })()`);

    const forbiddenRefRegex = new RegExp('ab' + 'ris', 'i');
    const htmlSourceRaw = fs.readFileSync(path.join(ROOT_DIR, 'polyglot_riff_studio_v3_1_atelier_edition.html'), 'utf8');
    const mdSourceRaw = fs.readFileSync(path.join(ROOT_DIR, 'checkpoint_and_wetwork_wbs_9x9.md'), 'utf8');
    check('Zero removed reference mentions in HTML source, Markdown spec, or rendered DOM',
      !forbiddenRefRegex.test(htmlSourceRaw) &&
      !forbiddenRefRegex.test(mdSourceRaw) &&
      !forbiddenRefRegex.test(lotusAudit.domTextLower) &&
      !lotusAudit.hasLegacyToggleDom &&
      !lotusAudit.hasSwitchFn
    );

    check('Lotus table has 9 rows and 81 cells', lotusAudit.rowCount === 9 && lotusAudit.cellCount === 81);
    check('Center cell [5,5] is "Polyglot Atelier Salesact" with core role',
      lotusAudit.grid[4][4].text === 'Polyglot Atelier Salesact' && lotusAudit.grid[4][4].role === 'core',
      lotusAudit.grid[4][4].text
    );
    check('Lotus header title, subtitle, description, Key, and Rules are populated',
      lotusAudit.title === '9 × 9 · Polyglot Atelier Salesact' &&
      lotusAudit.description.includes('centre block names eight themes around Polyglot Atelier Salesact') &&
      lotusAudit.keyText.startsWith('Key:') &&
      lotusAudit.rulesText.startsWith('Rules every cell obeys:')
    );
    check('All 9 Lotus radiation pills fit cleanly on a single row at 1440px viewport without orphan wrapping',
      lotusAudit.pillCount === 9 && lotusAudit.pillRowTops.length === 1,
      `pillRowTops=${JSON.stringify(lotusAudit.pillRowTops)}`
    );
    check('Default [5,5] Core state keeps all 16 theme headers uncluttered (0 twin-link rings until a theme is selected)',
      lotusAudit.coreTwinLinkedCount === 0
    );

    // Verify Center 3x3 ring <-> Outer 3x3 centers Lotus correspondence & 8 distinct theme accents
    const expectedPairs = [
      { t: 1, ring: [3, 3], outer: [1, 1], accent: 'lotus-theme-amber' },
      { t: 2, ring: [3, 4], outer: [1, 4], accent: 'lotus-theme-indigo' },
      { t: 3, ring: [3, 5], outer: [1, 7], accent: 'lotus-theme-emerald' },
      { t: 4, ring: [4, 3], outer: [4, 1], accent: 'lotus-theme-sky' },
      { t: 5, ring: [4, 5], outer: [4, 7], accent: 'lotus-theme-rose' },
      { t: 6, ring: [5, 3], outer: [7, 1], accent: 'lotus-theme-violet' },
      { t: 7, ring: [5, 4], outer: [7, 4], accent: 'lotus-theme-fuchsia' },
      { t: 8, ring: [5, 5], outer: [7, 7], accent: 'lotus-theme-teal' }
    ];
    for (const p of expectedPairs) {
      const ringCell = lotusAudit.grid[p.ring[0]][p.ring[1]];
      const outerCell = lotusAudit.grid[p.outer[0]][p.outer[1]];
      check(
        `Theme ${p.t} Center Ring [${p.ring[0] + 1},${p.ring[1] + 1}] matches Outer Block Center [${p.outer[0] + 1},${p.outer[1] + 1}] ("${ringCell.text}") with ${p.accent}`,
        ringCell.role === 'center-theme' &&
        outerCell.role === 'outer-theme' &&
        ringCell.text === outerCell.text &&
        ringCell.text.startsWith(`${p.t} · `) &&
        ringCell.className.includes(p.accent) &&
        outerCell.className.includes(p.accent)
      );
    }

    // Verify all 64 leaf cells are unique and non-empty, and HTML escaping preserved `< 2s`
    const leafTexts = lotusAudit.grid.flat().filter(c => c.role === 'leaf').map(c => c.text);
    check('All 64 leaf cells are non-empty and unique', leafTexts.length === 64 && new Set(leafTexts).size === 64);
    check('HTML special chars in ":COUNTERS_STATE < 2s" at [5,9] render literally without broken tags',
      lotusAudit.grid[4][8].text === ':COUNTERS_STATE < 2s' && lotusAudit.grid[4][8].childElemCount === 0,
      lotusAudit.grid[4][8].text
    );

    // Verify thicker 3x3 macro-block borders vs 1px inner cell borders
    const innerRight = parseFloat(lotusAudit.grid[0][0].borderRight);
    const macroRight3 = parseFloat(lotusAudit.grid[0][2].borderRight);
    const macroRight6 = parseFloat(lotusAudit.grid[0][5].borderRight);
    const edgeRight9 = parseFloat(lotusAudit.grid[0][8].borderRight);
    const innerBottom = parseFloat(lotusAudit.grid[0][0].borderBottom);
    const macroBottom3 = parseFloat(lotusAudit.grid[2][0].borderBottom);
    const macroBottom6 = parseFloat(lotusAudit.grid[5][0].borderBottom);
    const edgeBottom9 = parseFloat(lotusAudit.grid[8][0].borderBottom);
    check(
      'Macro 3x3 block dividers (cols 3 & 6, rows 3 & 6) have thicker borders than 1px inner cell hairlines',
      innerRight === 1 && macroRight3 > 1.5 && macroRight6 > 1.5 && edgeRight9 === 0 &&
      innerBottom === 1 && macroBottom3 > 1.5 && macroBottom6 > 1.5 && edgeBottom9 === 0,
      `inner=${innerRight}px, macroR=${macroRight3}px, macroB=${macroBottom3}px`
    );

    // Capture screenshot of Salesact 9x9 grid for visual inspection
    if (process.env.SAVE_SCREENSHOTS === '1') {
      const shot1 = await cdp.send('Page.captureScreenshot', { format: 'png' });
      fs.writeFileSync(path.join(ROOT_DIR, '.tmp_salesact_9x9.png'), Buffer.from(shot1.data, 'base64'));
    }

    // Test cell click, twin highlight, keyboard navigation, coordinate clamping, drill persistence, and deep-link navigation
    const interactionCheck = await cdp.eval(`(() => {
      // Click [1,2] fachat · šichta · fajront
      document.querySelector('#lotus-9x9-table td[data-row="1"][data-col="2"]').click();
      const insp12 = document.getElementById('lotus-inspector-content').textContent;
      const twinLinkedForTheme1 = document.querySelectorAll('#lotus-9x9-table .lotus-cell-twin-linked').length;
      const blockLinkedForTheme1 = document.querySelectorAll('#lotus-9x9-table .lotus-cell-block-linked').length;
      toggleLotusCellDrilled(1, 2);
      const badgeAfterDrill = document.getElementById('lotus-drilled-badge').textContent.trim();

      // Test boundary clamping on out-of-bounds & non-numeric inputs
      selectLotusCell(0, -10);
      const clampLow = selectedLotusCoord.slice();
      selectLotusCell(99, 42);
      const clampHigh = selectedLotusCoord.slice();
      selectLotusCell(NaN, undefined);
      const clampNaN = selectedLotusCoord.slice();
      const resolvedClamp = resolveLotusCell(-99, 99);

      // Test keyboard navigation & drill toggle on #lotus-9x9-table
      const tbl = document.getElementById('lotus-9x9-table');
      selectLotusCell(5, 5);
      tbl.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowRight', bubbles: true }));
      tbl.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowDown', bubbles: true }));
      const afterArrows = selectedLotusCoord.slice(); // expect [6, 6]
      tbl.dispatchEvent(new KeyboardEvent('keydown', { key: 'd', bubbles: true }));
      const badgeAfterKeyDrill = document.getElementById('lotus-drilled-badge').textContent.trim(); // expect 2/81
      tbl.dispatchEvent(new KeyboardEvent('keydown', { key: 'd', bubbles: true })); // unmark [6, 6]
      tbl.dispatchEvent(new KeyboardEvent('keydown', { key: 'Home', bubbles: true }));
      const afterHome = selectedLotusCoord.slice(); // expect [5, 5]

      // Click center ring [4,4] and test twin jump to [2,2]
      selectLotusCell(4, 4);
      const twinBefore = selectedLotusCoord.slice();
      selectLotusCell(2, 2);
      const twinAfter = selectedLotusCoord.slice();

      // Test connector deep-link from [8,1] Craig Ferguson -> Tab 3 Haute with FERGUSON active
      selectLotusCell(8, 1);
      runLotusSelectedAction();
      const inHaute = !document.getElementById('view-haute').classList.contains('hidden');
      const styleIsFerguson = activeComicStyle === 'FERGUSON';

      // Return to wetwork and test [3,1] -> Tab 4 Shield
      switchMode('wetwork');
      selectLotusCell(3, 1);
      runLotusSelectedAction();
      const inShield = !document.getElementById('view-shield').classList.contains('hidden');

      switchMode('wetwork');
      return {
        insp12,
        twinLinkedForTheme1,
        blockLinkedForTheme1,
        badgeAfterDrill,
        clampLow,
        clampHigh,
        clampNaN,
        resolvedClampCoords: [resolvedClamp.row, resolvedClamp.col],
        afterArrows,
        badgeAfterKeyDrill,
        afterHome,
        twinBefore,
        twinAfter,
        inHaute,
        styleIsFerguson,
        inShield
      };
    })()`);

    check('Clicking [1,2] updates Inspector with DE cognate notes, highlights 2 twin theme headers & 8 block leaves',
      interactionCheck.insp12.includes('Feierabend') &&
      interactionCheck.insp12.includes('db/cz_ova.db.json') &&
      interactionCheck.twinLinkedForTheme1 === 2 &&
      interactionCheck.blockLinkedForTheme1 === 8
    );
    check('Marking [1,2] drilled updates Drilled counter to 1/81', interactionCheck.badgeAfterDrill === 'Drilled: 1/81');
    check('Out-of-bounds and NaN coordinates clamp safely to [1..9] without throwing',
      interactionCheck.clampLow[0] === 1 && interactionCheck.clampLow[1] === 1 &&
      interactionCheck.clampHigh[0] === 9 && interactionCheck.clampHigh[1] === 9 &&
      interactionCheck.clampNaN[0] === 9 && interactionCheck.clampNaN[1] === 9 &&
      interactionCheck.resolvedClampCoords[0] === 1 && interactionCheck.resolvedClampCoords[1] === 9
    );
    check('Keyboard navigation (ArrowRight, ArrowDown, d drill toggle, Home) works cleanly on #lotus-9x9-table',
      interactionCheck.afterArrows[0] === 6 && interactionCheck.afterArrows[1] === 6 &&
      interactionCheck.badgeAfterKeyDrill === 'Drilled: 2/81' &&
      interactionCheck.afterHome[0] === 5 && interactionCheck.afterHome[1] === 5
    );
    check('Connector action on [8,1] deep-links to Tab 3 with Craig Ferguson lens active', interactionCheck.inHaute && interactionCheck.styleIsFerguson);
    check('Connector action on [3,1] deep-links to Tab 4 Interference Blitz', interactionCheck.inShield);

    // Edge cases: Wetwork 27m timer boundaries (03:00 Zero-English lock & 27:00 completion) + rapid clicks
    const timerCheck = await cdp.eval(`(() => {
      toggleWetworkTimer();
      toggleWetworkTimer(); // pause
      wetworkTimerSeconds = 180; // 03:00 boundary
      updateWetworkTimerUi();
      const at3Min = document.getElementById('wetwork-timer-phase-badge').textContent;
      wetworkTimerSeconds = 1620; // 27:00 completion boundary
      updateWetworkTimerUi();
      const at27Min = document.getElementById('wetwork-timer-phase-badge').textContent;
      resetWetworkTimer();
      const afterReset = document.getElementById('wetwork-timer-display').textContent;
      return { at3Min, at27Min, afterReset };
    })()`);
    check('Wetwork timer enforces Zero-English lock at 03:00 and completes cleanly at 27:00',
      timerCheck.at3Min.includes('ZERO-ENGLISH LOCK ACTIVE') &&
      timerCheck.at27Min.includes('Complete') &&
      timerCheck.afterReset === '00:00 / 27:00'
    );

    // Edge case: Legacy bare keys ('2_3') migrate to 'salesact_2_3', foreign keys scrub cleanly, missing fields self-heal across reload
    const foreignKeyName = 'ab' + 'ris_1_1';
    await cdp.eval(`(() => {
      const legacy = JSON.parse(localStorage.getItem('POLYGLOT_NEO4J_RIFF_STATE_V3_1'));
      legacy.lotusDrilled['2_3'] = true;
      legacy.lotusDrilled[${JSON.stringify(foreignKeyName)}] = true;
      delete legacy.wetworkChecks;
      delete legacy.wbsChecks;
      localStorage.setItem('POLYGLOT_NEO4J_RIFF_STATE_V3_1', JSON.stringify(legacy));
    })()`);
    await cdp.send('Page.reload');
    await new Promise(r => setTimeout(r, 250));
    await waitForAppReady(cdp);
    const postReloadCheck = await cdp.eval(`(() => {
      switchMode('wetwork');
      return {
        drilledBadge: document.getElementById('lotus-drilled-badge').textContent.trim(),
        wbsBadge: document.getElementById('wetwork-wbs-progress-badge').textContent.trim(),
        drilledKeys: Object.keys(state.lotusDrilled).sort()
      };
    })()`);
    check('Drilled cells persist, bare keys migrate to salesact_*, stale foreign keys scrub, and missing fields self-heal',
      postReloadCheck.drilledBadge === 'Drilled: 2/81' &&
      postReloadCheck.wbsBadge === 'Gates Passed: 12/26' &&
      JSON.stringify(postReloadCheck.drilledKeys) === JSON.stringify(['salesact_1_2', 'salesact_2_3']),
      JSON.stringify(postReloadCheck)
    );

    // Edge case: Corrupted JSON in localStorage
    await cdp.eval(`localStorage.setItem('POLYGLOT_NEO4J_RIFF_STATE_V3_1', '{corrupted_json')`);
    await cdp.send('Page.reload');
    await new Promise(r => setTimeout(r, 250));
    await waitForAppReady(cdp);
    const postCorruptCells = await cdp.eval(`switchMode('wetwork'); document.querySelectorAll('#lotus-9x9-table td').length`);
    check('Corrupted localStorage falls back gracefully and still renders 81 Lotus cells', postCorruptCells === 81);

    // Real pointer double-click (100ms human interval), pill/twin focus retention + real ArrowRight key, Persona bar sync, scroll clearance, and multi-viewport geometry
    await cdp.eval(`window.scrollTo(0, 0); selectLotusCell(5, 5);`);
    const rect13 = await cdp.eval(`(() => { const r = document.querySelector('#lotus-9x9-table td[data-row="1"][data-col="3"]').getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height / 2 }; })()`);
    await cdp.eval(`window.__dblRenderCount = 0; const _origRender = renderLotusGrid; renderLotusGrid = function() { window.__dblRenderCount++; return _origRender.apply(this, arguments); };`);
    await cdp.send('Input.dispatchMouseEvent', { type: 'mousePressed', x: rect13.x, y: rect13.y, button: 'left', clickCount: 1 });
    await cdp.send('Input.dispatchMouseEvent', { type: 'mouseReleased', x: rect13.x, y: rect13.y, button: 'left', clickCount: 1 });
    await new Promise(r => setTimeout(r, 100));
    await cdp.send('Input.dispatchMouseEvent', { type: 'mousePressed', x: rect13.x, y: rect13.y, button: 'left', clickCount: 2 });
    await cdp.send('Input.dispatchMouseEvent', { type: 'mouseReleased', x: rect13.x, y: rect13.y, button: 'left', clickCount: 2 });
    await new Promise(r => setTimeout(r, 80));
    const dblResult = await cdp.eval(`({ coord: selectedLotusCoord.slice(), badge: document.getElementById('lotus-drilled-badge').textContent.trim(), renders: window.__dblRenderCount })`);
    check(
      'Real human-timed pointer double-click on [1,3] drills cell with zero redundant DOM teardown (<= 2 renders)',
      dblResult.coord[0] === 1 && dblResult.coord[1] === 3 && dblResult.badge === 'Drilled: 1/81' && dblResult.renders <= 2,
      JSON.stringify(dblResult)
    );

    // Real pointer click on Radiation Pill #1 ('1 · CZ_OVA') -> real hardware ArrowRight key
    const pill1Rect = await cdp.eval(`(() => { const b = document.querySelectorAll('#lotus-theme-pills button')[1]; const r = b.getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height / 2 }; })()`);
    await cdp.send('Input.dispatchMouseEvent', { type: 'mousePressed', x: pill1Rect.x, y: pill1Rect.y, button: 'left', clickCount: 1 });
    await cdp.send('Input.dispatchMouseEvent', { type: 'mouseReleased', x: pill1Rect.x, y: pill1Rect.y, button: 'left', clickCount: 1 });
    await cdp.send('Input.dispatchKeyEvent', { type: 'rawKeyDown', key: 'ArrowRight', code: 'ArrowRight', windowsVirtualKeyCode: 39, nativeVirtualKeyCode: 39 });
    await cdp.send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'ArrowRight', code: 'ArrowRight', windowsVirtualKeyCode: 39, nativeVirtualKeyCode: 39 });
    const pillArrowRes = await cdp.eval(`({ coord: selectedLotusCoord.slice(), activeId: document.activeElement?.id })`);
    check(
      'Real pointer click on Radiation Pill retains focus on #lotus-9x9-table so real ArrowRight advances [2,2] -> [2,3]',
      pillArrowRes.activeId === 'lotus-9x9-table' && pillArrowRes.coord[0] === 2 && pillArrowRes.coord[1] === 3,
      JSON.stringify(pillArrowRes)
    );

    // Real pointer click on Inspector "Jump to Twin" -> real hardware ArrowRight key
    await cdp.eval(`selectLotusCell(2, 2);`);
    const twinBtnRect = await cdp.eval(`(() => { const b = Array.from(document.querySelectorAll('#lotus-inspector-content button')).find(x => x.textContent.includes('Twin')); b.scrollIntoView({ block: 'center' }); const r = b.getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height / 2 }; })()`);
    await cdp.send('Input.dispatchMouseEvent', { type: 'mousePressed', x: twinBtnRect.x, y: twinBtnRect.y, button: 'left', clickCount: 1 });
    await cdp.send('Input.dispatchMouseEvent', { type: 'mouseReleased', x: twinBtnRect.x, y: twinBtnRect.y, button: 'left', clickCount: 1 });
    await cdp.send('Input.dispatchKeyEvent', { type: 'rawKeyDown', key: 'ArrowRight', code: 'ArrowRight', windowsVirtualKeyCode: 39, nativeVirtualKeyCode: 39 });
    await cdp.send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'ArrowRight', code: 'ArrowRight', windowsVirtualKeyCode: 39, nativeVirtualKeyCode: 39 });
    const twinArrowRes = await cdp.eval(`({ coord: selectedLotusCoord.slice(), activeId: document.activeElement?.id })`);
    check(
      'Real pointer click on Inspector "Jump to Twin" retains focus on #lotus-9x9-table so ArrowRight advances [4,4] -> [4,5]',
      twinArrowRes.activeId === 'lotus-9x9-table' && twinArrowRes.coord[0] === 4 && twinArrowRes.coord[1] === 5,
      JSON.stringify(twinArrowRes)
    );

    // Top Persona bar click while on Tab 6 syncs Lotus theme + sticky header clearance + cross-tab scroll reset
    const navAndScrollRes = await cdp.eval(`(async () => {
      switchMode('wetwork');
      handlePersonaBarClick('AT_VIE');
      const personaLotusCoord = selectedLotusCoord.slice();

      // Sticky header clearance on intra-tab scroll action ([8,4] -> #wetwork-protocol-box)
      document.getElementById('wetwork-protocol-box').scrollIntoView({ behavior: 'instant', block: 'start' });
      const headerBottom = document.querySelector('header').getBoundingClientRect().bottom;
      const protocolTop = document.getElementById('wetwork-protocol-box').getBoundingClientRect().top;

      // Wetwork protocol [ ] checkbox single-line check
      const checkboxHeights = Array.from(document.querySelectorAll('#wetwork-protocol-list > div > span:first-child')).map(s => s.getBoundingClientRect().height);

      // Cross-tab deep-link scroll reset from bottom of Tab 6 -> Tab 3
      window.scrollTo(0, 1400);
      runTacticalRoom(3);
      const scrollAfterCrossTab = window.scrollY;
      const wetworkBtnHasRoseIdle = document.getElementById('btn-mode-wetwork').className.includes('text-rose-300');

      switchMode('wetwork');
      return { personaLotusCoord, headerBottom, protocolTop, maxCheckboxHeight: Math.max(...checkboxHeights), scrollAfterCrossTab, wetworkBtnHasRoseIdle };
    })()`);
    check(
      'Clicking AT_VIE Persona card while on Tab 6 focuses Theme 2 ([2,5])',
      navAndScrollRes.personaLotusCoord[0] === 2 && navAndScrollRes.personaLotusCoord[1] === 5
    );
    check(
      'Intra-tab scroll targets clear sticky <header> via scroll-mt-44 and [ ] checkboxes stay single-line',
      navAndScrollRes.protocolTop >= navAndScrollRes.headerBottom - 2 && navAndScrollRes.maxCheckboxHeight <= 24,
      JSON.stringify(navAndScrollRes)
    );
    check(
      'Cross-tab deep-link from scrolled Tab 6 resets window.scrollY to 0 and preserves tab accent colors',
      navAndScrollRes.scrollAfterCrossTab === 0 && navAndScrollRes.wetworkBtnHasRoseIdle,
      JSON.stringify(navAndScrollRes)
    );

    // Multi-viewport layout verification: 1024px & 1280px single-row pills + zero cell overflow, 375px mobile zero page blowout
    for (const vw of [1024, 1280]) {
      await cdp.send('Emulation.setDeviceMetricsOverride', { width: vw, height: 1000, deviceScaleFactor: 1.5, mobile: false });
      const vpAudit = await cdp.eval(`(() => {
        switchMode('wetwork');
        selectLotusCell(5, 5);
        const pillTops = Array.from(new Set(Array.from(document.querySelectorAll('#lotus-theme-pills button')).map(b => Math.round(b.getBoundingClientRect().top))));
        const overflows = Array.from(document.querySelectorAll('#lotus-9x9-table td')).filter(td => td.scrollHeight > td.clientHeight + 1 || td.scrollWidth > td.clientWidth + 1).length;
        return { pillRows: pillTops.length, overflows };
      })()`);
      check(`Viewport ${vw}px keeps all 9 Lotus Radiation pills on 1 row with 0 overflowing cells`, vpAudit.pillRows === 1 && vpAudit.overflows === 0, JSON.stringify(vpAudit));
    }

    await cdp.send('Emulation.setDeviceMetricsOverride', { width: 375, height: 812, deviceScaleFactor: 2, mobile: true });
    const mobileAudit = await cdp.eval(`(() => {
      switchMode('wetwork');
      window.scrollTo(0, 0);
      const wrap = document.getElementById('lotus-9x9-table').parentElement;
      wrap.scrollLeft = 500;
      const beforeLeft = wrap.scrollLeft;
      handleLotusCellClick(2, 9);
      const afterLeft = wrap.scrollLeft;
      return {
        docScrollWidth: document.documentElement.scrollWidth,
        beforeLeft,
        afterLeft,
        coord: selectedLotusCoord.slice()
      };
    })()`);
    check(
      'Mobile 375px viewport has zero horizontal page overflow (scrollWidth <= 375) and preserves table horizontal scrollLeft on right-side cell selection',
      mobileAudit.docScrollWidth <= 375 && mobileAudit.beforeLeft > 300 && mobileAudit.afterLeft === mobileAudit.beforeLeft && mobileAudit.coord[0] === 2 && mobileAudit.coord[1] === 9,
      JSON.stringify(mobileAudit)
    );

    // Restore 1440px desktop metrics and verify hyphenated tokens stay unbroken on 1 line
    await cdp.send('Emulation.setDeviceMetricsOverride', { width: 1440, height: 1200, deviceScaleFactor: 1.5, mobile: false });
    const hyphenAndRoomAudit = await cdp.eval(`(() => {
      switchMode('wetwork');
      const nowrapHeights = Array.from(document.querySelectorAll('#lotus-9x9-table td span.whitespace-nowrap')).map(s => Math.round(s.getBoundingClientRect().height));
      return {
        nowrapCount: nowrapHeights.length,
        maxNowrapHeight: Math.max(...nowrapHeights),
        room9Cz: TACTICAL_ROOMS[8].cz
      };
    })()`);
    check(
      'Hyphenated Lotus tokens (4-C, CP-1..CP-6, False-Friend, Silk-Gloved) never split across lines',
      hyphenAndRoomAudit.nowrapCount >= 10 && hyphenAndRoomAudit.maxNowrapHeight <= 20,
      JSON.stringify(hyphenAndRoomAudit)
    );

    // Markdown synchronization check against checkpoint_and_wetwork_wbs_9x9.md
    console.log('\n=== 3. Checking Synchronization with checkpoint_and_wetwork_wbs_9x9.md ===');
    const mdRaw = fs.readFileSync(path.join(ROOT_DIR, 'checkpoint_and_wetwork_wbs_9x9.md'), 'utf8');
    check(
      'Tactical Cross-Matrix Room 9 CZ_OVA phrase matches checkpoint_and_wetwork_wbs_9x9.md Section 3.1',
      hyphenAndRoomAudit.room9Cz === 'hoď na to oko, sfoukneme to' && mdRaw.includes(hyphenAndRoomAudit.room9Cz),
      hyphenAndRoomAudit.room9Cz
    );
    const sec32 = mdRaw.split('### 3.2')[1] || '';
    const mdTableRows = sec32
      .split(/\r?\n/)
      .filter(line => line.trim().startsWith('|') && !line.includes('Col 1') && !line.includes(':---:'))
      .slice(0, 9)
      .map(line => line.trim().replace(/^\||\|$/g, '').split('|').map(stripMdCellFormatting));

    check('Markdown Section 3.2 contains 9 rows x 9 cols (81 cells)',
      mdTableRows.length === 9 && mdTableRows.every(r => r.length === 9)
    );

    let mdMismatches = [];
    for (let r = 0; r < 9; r++) {
      for (let c = 0; c < 9; c++) {
        const htmlText = lotusAudit.grid[r][c].text;
        const mdText = mdTableRows[r][c];
        if (htmlText !== mdText) {
          mdMismatches.push(`[${r + 1},${c + 1}]: HTML="${htmlText}" vs MD="${mdText}"`);
        }
      }
    }
    check('All 81 Markdown 9x9 cells strictly match live HTML Polyglot Atelier Salesact grid',
      mdMismatches.length === 0,
      mdMismatches.join('; ')
    );

    check('Zero browser console errors & zero uncaught page exceptions across entire E2E run',
      cdp.consoleErrors.length === 0 && cdp.pageExceptions.length === 0,
      `consoleErrors=${JSON.stringify(cdp.consoleErrors)}, exceptions=${JSON.stringify(cdp.pageExceptions)}`
    );

    console.log(`\nALL ${passedChecks} AUTOMATED VERIFICATION CHECKS PASSED!`);
  } finally {
    if (cdp) cdp.close();
    proc.kill();
    server.close();
    await new Promise(r => setTimeout(r, 400));
    fs.rmSync(userDataDir, { recursive: true, force: true });
  }
}

main().catch((err) => {
  console.error('\nVERIFICATION FAILED:', err);
  process.exit(1);
});
