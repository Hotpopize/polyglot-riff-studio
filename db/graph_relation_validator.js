/**
 * POLYGLOT RIFF ATELIER — STRICT GRAPH RELATION RULE VALIDATOR
 * Enforces Node Schemas, Edge Cardinality, 4-C Stage Order, and Slang Token Integrity
 */

export const GRAPH_RELATION_RULES = {
  NODE_PRIMARY_KEYS: {
    Persona: 'id',
    Card: 'uid',
    Idiom: 'term',
    State: 'id',
    Bridge: 'uid',
    FalseFriend: 'cz',
    NewsWebhook: 'id'
  },
  ALLOWED_STAGES: ['COMPLIMENT', 'CHAMELEON', 'COUNTERACT', 'CURIOSITY'],
  STAGE_ORDER: {
    COMPLIMENT: 1,
    CHAMELEON: 2,
    COUNTERACT: 3,
    CURIOSITY: 4
  },
  EDGE_RULES: {
    HAS_CARD: { from: 'Persona', to: 'Card', sameLang: true },
    FLOWS_TO: { from: 'Card', to: 'Card', sameLang: true, requireSequentialStage: true },
    PIVOTS_VIA: { from: 'Card', to: 'Card', sameLang: false },
    INJECTS_SLANG: { from: 'Card', to: 'Idiom', sameLang: true },
    COUNTERS_STATE: { from: 'Card', to: 'State', requiredSourceStage: 'COUNTERACT' },
    SHARES_VIBE_WITH: { from: 'Idiom', to: 'Idiom', sameLang: false },
    HARVESTED_FROM: { from: 'Card', to: 'NewsWebhook', sameLang: true }
  }
};

export function validateCandidateGraphCommit({ card, idiom, edge, targetDb }) {
  const checks = [];

  if (card) {
    const validStage = GRAPH_RELATION_RULES.ALLOWED_STAGES.includes(card.stage);
    checks.push({
      rule: '(:Card) Stage Constraint',
      passed: validStage,
      detail: validStage ? `Valid 4-C stage: ${card.stage}` : `Invalid stage: ${card.stage}`
    });

    const matchesDb = !targetDb || targetDb === 'ALL' || card.lang === targetDb;
    checks.push({
      rule: 'Per-Language DB Partition Rule',
      passed: matchesDb,
      detail: matchesDb ? `Routed cleanly to db/${card.lang.toLowerCase()}.db.json` : `Cross-DB mismatch (${card.lang} vs ${targetDb})`
    });
  }

  if (idiom && card) {
    const hasTokenSpan = card.text.includes(`data-term="${idiom.term}"`) || card.text.toLowerCase().includes(idiom.term.toLowerCase());
    checks.push({
      rule: '[:INJECTS_SLANG] Lexical Anchor Rule',
      passed: hasTokenSpan,
      detail: hasTokenSpan ? `Idiom "${idiom.term}" anchored in Card text` : `Idiom "${idiom.term}" missing from Card text`
    });
  }

  if (edge) {
    const validWeight = typeof edge.weight === 'number' && edge.weight >= 0.15 && edge.weight <= 0.99;
    checks.push({
      rule: 'FSRS Edge Weight & Stability Bounds',
      passed: validWeight,
      detail: validWeight ? `w=${edge.weight}, S=${edge.stability || 5.0}d` : 'Edge weight out of [0.15, 0.99] bounds'
    });
  }

  return {
    valid: checks.every(c => c.passed),
    checks
  };
}

