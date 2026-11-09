// 1. Seed Room-Friction Objection States (:State)
UNWIND [
  {id: 'PLAYING_IT_SAFE', desc: 'Counterpart is hiding behind legacy workflows or incrementalism'},
  {id: 'OVERTHINKING', desc: 'Analysis paralysis or waiting for the "perfect moment"'},
  {id: 'CORPORATE_SHIELD', desc: 'Stiff executive formality blocking real technical candor'},
  {id: 'MANUAL_GRIND', desc: 'Team is burning hours on repetitive pipeline handoffs'}
] AS stData
MERGE (s:State {id: stData.id})
SET s.description = stData.desc;

// 2. Wire [:COUNTERS_STATE] from your 5 Regional [COUNTERACT] Cards
MATCH (cOva:Card {uid: 'CZ_OVA_COUNT'}), (sGrind:State {id: 'MANUAL_GRIND'})
MERGE (cOva)-[:COUNTERS_STATE {effectiveness: 0.96, cue: 'Clip vowels, lean forearms on table'}]->(sGrind);

MATCH (cVie:Card {uid: 'AT_VIE_COUNT'}), (sShield:State {id: 'CORPORATE_SHIELD'})
MERGE (cVie)-[:COUNTERS_STATE {effectiveness: 0.94, cue: 'Wry grin, coat-check wave'}]->(sShield);

MATCH (cAla:Card {uid: 'RU_ALA_COUNT'}), (sOver:State {id: 'OVERTHINKING'})
MERGE (cAla)-[:COUNTERS_STATE {effectiveness: 0.95, cue: 'Deep chest voice, slow down'}]->(sOver);

MATCH (cYyc:Card {uid: 'EN_YYC_COUNT'}), (sSafe:State {id: 'PLAYING_IT_SAFE'})
MERGE (cYyc)-[:COUNTERS_STATE {effectiveness: 0.93, cue: 'Half-octave drop, accomplice smirk'}]->(sSafe);

MATCH (cSot:Card {uid: 'ES_SOT_COUNT'}), (sSafe2:State {id: 'PLAYING_IT_SAFE'})
MERGE (cSot)-[:COUNTERS_STATE {effectiveness: 0.91, cue: 'High-energy Andaluz challenge'}]->(sSafe2);

// 3. Seed Extended Tri-Lingual Interference Shield (:FalseFriend)
UNWIND [
  {cz: 'úžasný', ru_trap: 'ужасный (terrible)', de_calque: 'erstaunlich / großartig', meaning: 'amazing / impressive'},
  {cz: 'čerstvý', ru_trap: 'черствый (stale)', de_calque: 'frisch / aktuell', meaning: 'fresh / real-time (čerstvá data)'},
  {cz: 'nápad', ru_trap: 'нападки (attacks)', de_calque: 'Einfall (ná-pad)', meaning: 'idea / architectural concept'},
  {cz: 'vyprodat', ru_trap: 'распродать (sell out)', de_calque: 'ausverkaufen', meaning: 'liquidate stock (never use for B2B selling)'},
  {cz: 'pozor', ru_trap: 'позор (shame)', de_calque: 'Achtung / Vorsicht', meaning: 'attention (dávat pozor na = achten auf)'},
  {cz: 'hodina', ru_trap: 'година (year/era)', de_calque: 'Stunde', meaning: 'one hour (critical for SLA commitments)'},
  {cz: 'zapomenout', ru_trap: 'запомнить (remember)', de_calque: 'vergessen', meaning: 'to forget (exact opposite of Russian запомнить)'},
  {cz: 'přesný', ru_trap: 'пресный (bland/unseasoned)', de_calque: 'präzise / genau', meaning: 'exact / deterministic (přesná data)'},
  {cz: 'směšný', ru_trap: 'смешной (funny)', de_calque: 'lächerlich', meaning: 'ridiculous / absurd (carries negative weight in B2B)'}
] AS ff
MERGE (f:FalseFriend {cz_term: ff.cz})
SET f += ff;