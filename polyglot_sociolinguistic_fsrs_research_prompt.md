Act as a Principal Computational Linguist, Sociolinguist, and Graph Systems Architect. Conduct an exhaustive, multi-disciplinary literature review and empirical corpus synthesis to expand a stateful Neo4j conversational training engine ("Polyglot Interpersonal Riff Studio"). 

The system models high-rapport interpersonal banter and B2B technical framing across a 4-stage state machine—1. Compliment (validating craft), 2. Chameleon (phonetic/grammatical alignment), 3. Counteract (status-equalizing pushback/pattern interrupt), and 4. Curiosity (open-loop hooks)—across five specific regional registers:
1. CZ_OVA / CZ_STD: Ostravian Working Register (Ostravština / Moravian-Silesian industrial contact) vs. Codified Standard Czech (Spisovná čeština).
2. AT_VIE: Viennese German (Wiener Schmäh / Austro-Bavarian Kaffeehaus register).
3. RU_ALA: Almaty Russian (Южная Столица Slavic-Turkic contact register).
4. EN_YYC: Western Canadian English (Calgary / Foothills straight-shooter register).
5. ES_SOT: Western Andalusian / Costa del Sol Spanish (Sotogrande high-register Andaluz).

Deliver a structured synthesis with academic citations, authentic lexical corpora, acoustic benchmarks, and mathematical formulas across the following five research pillars:

### PILLAR 1: Regional Sociolinguistic & Pragmatic Corpora
For each of the 5 regional personas, extract documented discourse markers, syntactic intimacy triggers, and register-shifting rules:
* Czech (Ostravština vs. Spisovná čeština): Literature on Silesian-Czech phonetics (vowel shortening, fixed penultimate/first-syllable stress competition), German industrial/mining loanwords in the Ostrava basin (e.g., šichta, fajront, fachat), Silesian particles (causal "bo", spatial "kaj"), and B2B register switching between formal vykání (with 5th-case Vocative addressing and German-calqued prepositional governance like zaměřit se na, spoléhat se na) and engineering tykání.
* Viennese German (Wiener Schmäh): Pragmatic analyses of Austro-Bavarian modal particles (eh, halt, ja, wohl), ironic understatement as status equalization, and coffeehouse/Beisl idioms (e.g., G’schichtldrucken, schwer in Ordnung).
* Almaty Russian (Slavic-Turkic Contact): Sociolinguistic studies on Southern Kazakhstan urban Russian, Turkic/Kazakh pragmatic borrowing (kinship vocatives like родной/брат, hospitality framing around дастархан), and zero-copula high-trust directness.
* Western Canadian English (Calgary/Alberta): Lexical and phonetic markers of Foothills/Prairie Canadian English, blue-collar-meets-executive mechanical metaphors, and disarming solidarity vocatives ("bud").
* Andalusian Spanish (Sotogrande/Cádiz-Málaga): Pragmatics of high-register Southern Peninsular Spanish, conspiratorial subjunctive triggers, sensory hyperbole, and duende/taurine metaphors in social persuasion.

### PILLAR 2: Cross-Linguistic Etymology & Trilingual Interference (CZ / RU / DE)
* Map the Central European etymological network connecting Austrian German, Czech/Silesian, and Russian (shared industrial, military, and cultural loanwords) to populate (:Idiom)-[:SHARES_VIBE_WITH]->(:Idiom) graph edges.
* Compile an empirical matrix of high-risk Slavic false friends (mezijazyková homonymie) between Russian and Czech, alongside their German structural calques, that frequently derail technical or B2B discussions (expanding beyond úžasný, čerstvý, nápad, vyprodat, pozor, hodina).

### PILLAR 3: Conversation Analysis (CA) & Acoustic Prosody of the "4 Cs"
* Locate Conversation Analysis (CA) and psycholinguistic literature on pattern interrupts, status-equalizing pushbacks ("Velvet Pushback" / Counteract), and Communication Accommodation Theory (Chameleon effect) in high-stakes persuasion.
* Provide quantifiable acoustic-prosodic benchmarks suitable for real-time Web Audio API extraction:
  - Fundamental frequency (F0) pitch drop ratios (in semitones/octaves) that signal warmth vs. dominance during pushbacks.
  - Syllable-per-second (speech rate) and vowel duration ratios distinguishing clipped Ostravian Czech (CZ_OVA) from Standard Czech (CZ_STD) and Viennese German (AT_VIE).
  - Syntactic constraints (Matrix Language Frame model by Myers-Scotton) for smooth mid-sentence code-switching (:Bridge nodes) so switches occur at natural syntactic boundaries without breaking rhythm.

### PILLAR 4: Graph-Based Spaced Repetition (SRS) & Edge-Decay Mathematics
* Review mathematical models for Spaced Repetition Systems applied to sequential transition graphs (Markov chains / property graphs) rather than isolated flashcards—specifically comparing FSRS (Free Spaced Repetition Scheduler), SM-17, and Half-Life Regression (HLR) for edge weighting.
* Formulate an upgraded edge-mastery update and time-decay equation for Neo4j [:FLOWS_TO] and [:PIVOTS_VIA] relationships that improves upon linear clamping:
  w_new = clamp(w_old + (score - 3) * 0.07, 0.15, 0.99)
  Incorporate edge retrievability R(t), stability S, difficulty D, and path-propagation weights for multi-hop Cypher traversals.

### PILLAR 5: Required Output Schema (Neo4j Ready)
Format all extracted linguistic and pragmatic findings into structured tables and Cypher-ready JSON blocks containing:
1. Citation & Source Context (Author, Year, Study/Corpus Name).
2. Exact Regional Phrase / Idiom + Phonetic/Acoustic Delivery Rule.
3. Etymological Root & Cross-Language Cousin (for :SHARES_VIBE_WITH wiring).
4. Target 4-C Stage (COMPLIMENT, CHAMELEON, COUNTERACT, CURIOSITY) or Objection State (:COUNTERS_STATE -> GUARDED | SKEPTICAL | PLAYING_IT_SAFE).