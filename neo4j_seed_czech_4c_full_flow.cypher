// 1. Create Constraints & Indexes for Czech Personas
CREATE CONSTRAINT cz_persona_id IF NOT EXISTS FOR (p:Persona) REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT cz_card_uid IF NOT EXISTS FOR (c:Card) REQUIRE c.uid IS UNIQUE;

// 2. Seed the Two Czech Operational Personas
UNWIND [
  {
    id: 'CZ_STD',
    name: 'Spisovná Čeština (Executive B2B)',
    family: 'West Slavic (High Register)',
    register: 'Vykání / C-Suite',
    phonetics: 'Precise vowel length, standard grammar, formal address',
    trick: 'German-aligned prepositional governance (zaměřit se na, spoléhat se na)'
  },
  {
    id: 'CZ_OVA',
    name: 'Ostravština (Industrial Tech Peer)',
    family: 'West Slavic / Silesian-German Contact',
    register: 'Tykání / Engineering Trench',
    phonetics: 'Clipped short vowels, heavy first-syllable stress',
    trick: 'Austrian industrial loanwords (fachat, šichta, fajront) + causal "bo"'
  }
] AS czData
MERGE (p:Persona {id: czData.id})
SET p += czData;

// 3. Seed Conversational Riff Cards (4-C Structure across Registers)
MERGE (c1:Card {uid: 'CZ_STD_COMP_01'})
SET c1.stage = 'COMPLIMENT',
    c1.lang = 'CZ_STD',
    c1.text = 'Sleduji, v jakém měřítku teď v týmu škálujete produkci – málokdo na trhu má takhle čistě zvládnutou exekuci.',
    c1.energy = 2,
    c1.vibe = 'High-Warmth / Low-Guard'

MERGE (c2:Card {uid: 'CZ_STD_CHAM_01'})
SET c2.stage = 'CHAMELEON',
    c2.lang = 'CZ_STD',
    c2.text = 'Vím, že přemýšlíte v metrikách návratnosti a nechcete do firmy tahat zbytečný bloatware, který by lidi jen zpomaloval.',
    c2.energy = 3,
    c2.vibe = 'High-Warmth / Low-Guard'

// The Bridge Node handling the register drop from Prague boardroom to Ostrava dev floor
MERGE (bBridge:Bridge {uid: 'BR_CZ_STD_TO_OVA'})
SET bBridge.from_lang = 'CZ_STD',
    bBridge.to_lang = 'CZ_OVA',
    bBridge.text = 'A když teď odložíme kravaty a podíváme se přímo pod kapotu s klukama z vývoje—',
    bBridge.transition_type = 'REGISTER_DROP'

MERGE (c3:Card {uid: 'CZ_OVA_COUNT_01'})
SET c3.stage = 'COUNTERACT',
    c3.lang = 'CZ_OVA',
    c3.text = 'Máte to postavené fajně, ale to ruční překlápění dat je zbytečná šichta navíc. Jak nasadíme náš modul, bude to fachat samo a kluci můžou mít v klidu fajront, bo skript to pohlídá za ně.',
    c3.energy = 4,
    c3.vibe = 'Pragmatic Engineering Disruption'

MERGE (c4:Card {uid: 'CZ_OVA_CUR_01'})
SET c4.stage = 'CURIOSITY',
    c4.lang = 'CZ_OVA',
    c4.text = 'Hoď na to oko v příloze, a jestli to dává smysl, brnkni mi zítra dopoledne a sfoukneme to.',
    c4.energy = 3,
    c4.vibe = 'Action-Oriented Hook'

// 4. Seed Linguistic / Slang Nodes
UNWIND [
  {term: 'fachat', origin: 'German: Fach/fachen', delivery: 'Crisp, percussive first syllable'},
  {term: 'šichta', origin: 'German: Schicht', delivery: 'Grounded, heavy industrial weight'},
  {term: 'fajront', origin: 'German: Feierabend', delivery: 'Relaxed downward inflection, exhale'},
  {term: 'bo', origin: 'Silesian causal particle', delivery: 'Quick connector meaning "protože"'}
] AS slang
MERGE (i:Idiom {term: slang.term})
SET i += slang
WITH i, c3
MERGE (c3)-[:INJECTS_SLANG {slot: 'impact_phrase'}]->(i);

// 5. Wire Graph Traversal Flow
MERGE (c1)-[:FLOWS_TO {weight: 0.95}]->(c2)
MERGE (c2)-[:PIVOTS_VIA {weight: 0.98}]->(bBridge)
MERGE (bBridge)-[:LANDS_ON]->(c3)
MERGE (c3)-[:FLOWS_TO {weight: 0.90}]->(c4);