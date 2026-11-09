// 1. Seed the Two Czech Personas
UNWIND [
  {
    id: 'CZ_STD',
    name: 'Spisovná Čeština (Executive B2B)',
    family: 'West Slavic (High Register)',
    register: 'Vykání / C-Suite',
    trick: 'Vocative case addressing + German-calqued prepositional government (zaměřit se na, spoléhat se na)'
  },
  {
    id: 'CZ_OVA',
    name: 'Ostravský Pracovní Registr (Tech Peer)',
    family: 'West Slavic / Silesian-German Industrial Contact',
    register: 'Tykání / Engineering Trench',
    trick: 'Clipped short vowels + Austrian industrial loanwords (fachat, šichta, fajront) + causal "bo"'
  }
] AS czPersonas
MERGE (p:Persona {id: czPersonas.id})
SET p += czPersonas;

// 2. Seed Czech B2B Cards & Code-Switch Bridge (Executive -> Engineering Pivot)
MERGE (cExec:Card {uid: 'CZ_STD_COMP_01'})
SET cExec.stage = 'COMPLIMENT',
    cExec.lang = 'CZ_STD',
    cExec.text = 'Sleduji, v jakém měřítku teď v týmu škálujete produkci – málokdo na trhu má takhle čistě zvládnutou exekuci.',
    cExec.energy = 2

MERGE (bTechPivot:Bridge {uid: 'BR_CZ_STD_TO_OVA'})
SET bTechPivot.from_lang = 'CZ_STD',
    bTechPivot.to_lang = 'CZ_OVA',
    bTechPivot.text = 'A když teď odložíme kravaty a podíváme se přímo pod kapotu s klukama z vývoje—'

MERGE (cOvaCount:Card {uid: 'CZ_OVA_COUNT_01'})
SET cOvaCount.stage = 'COUNTERACT',
    cOvaCount.lang = 'CZ_OVA',
    cOvaCount.text = 'Máte to postavené fajně, ale to ruční překlápění dat je zbytečná šichta navíc. Jak nasadíme náš modul, bude to fachat samo a kluci můžou mít v klidu fajront, bo skript to pohlídá za ně.',
    cOvaCount.energy = 4

// 3. Attach Regional Silesian/Industrial Idioms
UNWIND [
  {term: 'fachat', origin: 'German: Fach/fachen', delivery: 'Crisp, short vowels, first-syllable punch'},
  {term: 'fajront', origin: 'German: Feierabend', delivery: 'Relaxed exhale, downward inflection'},
  {term: 'bo', origin: 'Silesian causal particle', delivery: 'Quick unstressed connector meaning "protože"'}
] AS ovaIdioms
MERGE (i:Idiom {term: ovaIdioms.term})
SET i += ovaIdioms
WITH i, cOvaCount
MERGE (cOvaCount)-[:INJECTS_SLANG]->(i);

// 4. Wire the Traversal Path
MATCH (cExec:Card {uid: 'CZ_STD_COMP_01'}),
      (bTechPivot:Bridge {uid: 'BR_CZ_STD_TO_OVA'}),
      (cOvaCount:Card {uid: 'CZ_OVA_COUNT_01'})
MERGE (cExec)-[:PIVOTS_VIA {weight: 0.94, context: 'C-Suite_to_Dev_Handoff'}]->(bTechPivot)
MERGE (bTechPivot)-[:LANDS_ON]->(cOvaCount);