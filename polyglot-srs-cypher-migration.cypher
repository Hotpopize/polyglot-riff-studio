// ============================================================================
// NEO4J SRS GRAPH MIGRATION: POLYGLOT REGIONAL & FORMAL REGISTER BRIDGES + CITY ANTHEMS
// Version: 3.3
// Includes: IB Past Paper Formal Registers (CZ, DE, RU, EN, ES) + 4-C Personas
//           + Vocabulary Nodes + Regional City Anthems & Cross-Lingual Lyric Translations
//           + Cross-Register Code-Switch Bridges + False Friend Alerts
//           + Global Track: The Weeknd ft. JENNIE & Lily-Rose Depp - "One of the Girls"
// ============================================================================

// ----------------------------------------------------------------------------
// 1. CONSTRAINTS & INDEXES
// ----------------------------------------------------------------------------
CREATE CONSTRAINT card_uid IF NOT EXISTS FOR (c:Card) REQUIRE c.uid IS UNIQUE;
CREATE CONSTRAINT persona_id IF NOT EXISTS FOR (p:Persona) REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT register_id IF NOT EXISTS FOR (r:Register) REQUIRE r.id IS UNIQUE;
CREATE CONSTRAINT vocab_uid IF NOT EXISTS FOR (v:Vocab) REQUIRE v.uid IS UNIQUE;
CREATE CONSTRAINT bridge_uid IF NOT EXISTS FOR (b:Bridge) REQUIRE b.uid IS UNIQUE;
CREATE CONSTRAINT song_uid IF NOT EXISTS FOR (s:Song) REQUIRE s.uid IS UNIQUE;

// ----------------------------------------------------------------------------
// 2. SEED REGIONAL PERSONAS
// ----------------------------------------------------------------------------
MERGE (p_CZ_OVA:Persona {id: 'CZ_OVA'})
  SET p_CZ_OVA.name = 'Ostravština',
      p_CZ_OVA.family = 'West Slavic + Austrian Industrial Contact',
      p_CZ_OVA.rhythm = 'Clipped short vowels, uncompromising first-syllable stress',
      p_CZ_OVA.trick = 'Mining Germanisms + Silesian causal particle "bo"';

MERGE (p_AT_VIE:Persona {id: 'AT_VIE'})
  SET p_AT_VIE.name = 'Wiener Schmäh',
      p_AT_VIE.family = 'Austro-Bavarian',
      p_AT_VIE.rhythm = 'Syncopated waltz cadence, stretched vowels on ironic understatements',
      p_AT_VIE.trick = 'Modal particles (eh, halt, ja, mal) + Kaffeehaus irony';

MERGE (p_RU_ALA:Persona {id: 'RU_ALA'})
  SET p_RU_ALA.name = 'Almaty Insider',
      p_RU_ALA.family = 'Slavic-Turkic Contact',
      p_RU_ALA.rhythm = 'Deep chest resonance, warm openings, decisive pivots',
      p_RU_ALA.trick = 'Kinship vocatives (родной) + Kazakhstani hospitality metaphors';

MERGE (p_EN_YYC:Persona {id: 'EN_YYC'})
  SET p_EN_YYC.name = 'Calgary Flair',
      p_EN_YYC.family = 'Anglo-Germanic (Western Canadian)',
      p_EN_YYC.rhythm = 'Percussive monosyllabic punch, warm gravel, zero pretension',
      p_EN_YYC.trick = 'Mechanical metaphors (all hat and no cattle, give ’er)';

MERGE (p_ES_SOT:Persona {id: 'ES_SOT'})
  SET p_ES_SOT.name = 'Sotogrande Duende',
      p_ES_SOT.family = 'Iberian Romance (Andaluz High Register)',
      p_ES_SOT.rhythm = 'Rapid melodic bursts followed by sun-soaked pauses',
      p_ES_SOT.trick = 'Conspiratorial subjunctive mood + sensory hyperbole (tiene duende)';

// ----------------------------------------------------------------------------
// 3. SEED FORMAL & REGIONAL REGISTER NODES
// ----------------------------------------------------------------------------
MERGE (r_CZ_FORMAL:Register {id: 'CZ_FORMAL_IB'})
  SET r_CZ_FORMAL.lang = 'CZ', r_CZ_FORMAL.type = 'FORMAL_EXAM', r_CZ_FORMAL.name = 'Spisovná Čeština (IB Academic & Executive B2B)';
MERGE (r_CZ_REGIONAL:Register {id: 'CZ_REGIONAL_OVA'})
  SET r_CZ_REGIONAL.lang = 'CZ', r_CZ_REGIONAL.type = 'REGIONAL_RIFF', r_CZ_REGIONAL.name = 'Ostravská Pracovní Řeč';

MERGE (r_DE_FORMAL:Register {id: 'DE_FORMAL_IB'})
  SET r_DE_FORMAL.lang = 'DE', r_DE_FORMAL.type = 'FORMAL_EXAM', r_DE_FORMAL.name = 'Hochdeutsch (IB Textanalyse & B2B Exec)';
MERGE (r_DE_REGIONAL:Register {id: 'DE_REGIONAL_VIE'})
  SET r_DE_REGIONAL.lang = 'DE', r_DE_REGIONAL.type = 'REGIONAL_RIFF', r_DE_REGIONAL.name = 'Wiener Kaffeehaus-Schmäh';

MERGE (r_RU_FORMAL:Register {id: 'RU_FORMAL_IB'})
  SET r_RU_FORMAL.lang = 'RU', r_RU_FORMAL.type = 'FORMAL_EXAM', r_RU_FORMAL.name = 'Академический Русский (IB Литературный разбор)';
MERGE (r_RU_REGIONAL:Register {id: 'RU_REGIONAL_ALA'})
  SET r_RU_REGIONAL.lang = 'RU', r_RU_REGIONAL.type = 'REGIONAL_RIFF', r_RU_REGIONAL.name = 'Алматинский Разговорный Регистр';

MERGE (r_EN_FORMAL:Register {id: 'EN_FORMAL_IB'})
  SET r_EN_FORMAL.lang = 'EN', r_EN_FORMAL.type = 'FORMAL_EXAM', r_EN_FORMAL.name = 'Academic English (IB Rhetorical Analysis)';
MERGE (r_EN_REGIONAL:Register {id: 'EN_REGIONAL_YYC'})
  SET r_EN_REGIONAL.lang = 'EN', r_EN_REGIONAL.type = 'REGIONAL_RIFF', r_EN_REGIONAL.name = 'Calgary Foothills Working Register';

MERGE (r_ES_FORMAL:Register {id: 'ES_FORMAL_IB'})
  SET r_ES_FORMAL.lang = 'ES', r_ES_FORMAL.type = 'FORMAL_EXAM', r_ES_FORMAL.name = 'Español Académico (IB Análisis Literario)';
MERGE (r_ES_REGIONAL:Register {id: 'ES_REGIONAL_SOT'})
  SET r_ES_REGIONAL.lang = 'ES', r_ES_REGIONAL.type = 'REGIONAL_RIFF', r_ES_REGIONAL.name = 'Sotogrande Andaluz Coloquial';

// Connect Personas to Registers
MATCH (p:Persona {id: 'CZ_OVA'}), (r:Register {id: 'CZ_REGIONAL_OVA'}) MERGE (p)-[:EMBODIES_REGISTER]->(r);
MATCH (p:Persona {id: 'AT_VIE'}), (r:Register {id: 'DE_REGIONAL_VIE'}) MERGE (p)-[:EMBODIES_REGISTER]->(r);
MATCH (p:Persona {id: 'RU_ALA'}), (r:Register {id: 'RU_REGIONAL_ALA'}) MERGE (p)-[:EMBODIES_REGISTER]->(r);
MATCH (p:Persona {id: 'EN_YYC'}), (r:Register {id: 'EN_REGIONAL_YYC'}) MERGE (p)-[:EMBODIES_REGISTER]->(r);
MATCH (p:Persona {id: 'ES_SOT'}), (r:Register {id: 'ES_REGIONAL_SOT'}) MERGE (p)-[:EMBODIES_REGISTER]->(r);

// ----------------------------------------------------------------------------
// 4. REGIONAL CITY ANTHEMS & CROSS-LINGUAL LYRIC TRANSLATIONS (:Song)
// ----------------------------------------------------------------------------

// 1. OSTRAVA (CZECH REPUBLIC): Jaromír Nohavica - "Ostrava"
MERGE (s_CZ_OVA:Song {uid: 'SONG_CZ_OVA_NOHAVICA'})
  SET s_CZ_OVA.title = 'Ostrava',
      s_CZ_OVA.artist = 'Jaromír Nohavica',
      s_CZ_OVA.city_region = 'Ostrava (Moravian-Silesian Region)',
      s_CZ_OVA.genre = 'Regional Industrial Folk / Bard',
      s_CZ_OVA.original_lyric = 'Ostrava, Ostrava, město mezi městy, kaj ľudzie fchytaju šichtu a po robotě maju čistý fajront, bo ten motor pojede sám.',
      s_CZ_OVA.original_lang = 'CZ_OVA',
      s_CZ_OVA.translation_es = 'Ostrava, Ostrava, ciudad entre ciudades, donde la gente agarra el turno de trabajo y tras la labor tiene el fajront limpio, porque el motor funcionará solo.',
      s_CZ_OVA.translation_en = 'Ostrava, Ostrava, city among cities, where people catch their shift and after work enjoy clean quitting time, because the engine will run by itself.',
      s_CZ_OVA.translation_de = 'Ostrava, Ostrava, Stadt unter Städten, wo die Leute ihre Schicht anpacken und nach der Arbeit sauberen Feierabend haben, weil der Motor von alleine läuft.',
      s_CZ_OVA.cultural_vibe = 'Industrial pride, miner grit, uncompromising short-vowel pace';

// 2. VIENNA (AUSTRIA): Falco - "Vienna Calling"
MERGE (s_AT_VIE:Song {uid: 'SONG_AT_VIE_FALCO'})
  SET s_AT_VIE.title = 'Vienna Calling',
      s_AT_VIE.artist = 'Falco (Johann Hölzel)',
      s_AT_VIE.city_region = 'Vienna (Austro-Bavarian)',
      s_AT_VIE.genre = 'Austropop / Viennese New Wave',
      s_AT_VIE.original_lyric = 'Vienna Calling! Oida, die Zeit rennt davon. Kein Stress, der Schmäh rennt eh von allein, musst nur die Vorsicht an der Garderobe abgeben.',
      s_AT_VIE.original_lang = 'AT_VIE',
      s_AT_VIE.translation_es = '¡Llamada desde Viena! Oida, el tiempo se nos va. Cero estrés, el encanto vienés fluye solo de todos modos, solo debes dejar la cautela en el ropero.',
      s_AT_VIE.translation_en = 'Vienna Calling! Oida, time is running away. No stress, the Schmäh runs on its own anyway, you just have to leave caution at the coat check.',
      s_AT_VIE.translation_cz = 'Vídeň volá! Oida, čas utíká. Žádný stres, ten Schmäh stejně běží sám od sebe, jen musíš nechat opatrnost v šatně.',
      s_AT_VIE.cultural_vibe = 'Syncopated coffeehouse charm, theatrical detachment, status equalization';

// 3. ALMATY (KAZAKHSTAN): A-Studio / Batyrkhan Shukenov - "Джулия" (Julia)
MERGE (s_RU_ALA:Song {uid: 'SONG_RU_ALA_ASTUDIO'})
  SET s_RU_ALA.title = 'Джулия (Julia)',
      s_RU_ALA.artist = 'A-Studio (Batyrkhan Shukenov)',
      s_RU_ALA.city_region = 'Almaty (Southern Capital / Медео)',
      s_RU_ALA.genre = 'Almaty Synth-Pop / Kazakhstani Soul',
      s_RU_ALA.original_lyric = 'Девочка моя Джулия, под тёплыми звёздами Алматы мы всё сделаем по красоте, базару нет, как за широким дастарханом.',
      s_RU_ALA.original_lang = 'RU_ALA',
      s_RU_ALA.translation_es = 'Mi chica Julia, bajo las cálidas estrellas de Almaty lo haremos todo con pura belleza, sin duda alguna, como en un gran dastarhan.',
      s_RU_ALA.translation_en = 'My girl Julia, under the warm stars of Almaty we will do everything with absolute beauty, zero doubt, like at a wide dastarhan.',
      s_RU_ALA.translation_de = 'Mein Mädchen Julia, unter den warmen Sternen von Almaty machen wir alles mit wahrer Schönheit, ohne Zweifel, wie an einem großen Dastarhan.',
      s_RU_ALA.cultural_vibe = 'Terrace warmth, Kazakhstani hospitality, soul-driven execution';

// 4. CALGARY (CANADA): Loverboy - "Working for the Weekend"
MERGE (s_EN_YYC:Song {uid: 'SONG_EN_YYC_LOVERBOY'})
  SET s_EN_YYC.title = 'Working for the Weekend',
      s_EN_YYC.artist = 'Loverboy',
      s_EN_YYC.city_region = 'Calgary & Western Canada',
      s_EN_YYC.genre = 'Western Canadian Arena Rock',
      s_EN_YYC.original_lyric = 'Everybody is working for the weekend, bud! Stop being all hat and no cattle, kick the garage door open and just give ’er!',
      s_EN_YYC.original_lang = 'EN_YYC',
      s_EN_YYC.translation_es = '¡Todo el mundo trabaja para el fin de semana, viejo! Déjate de postureo sin sustancia, abre la puerta del garaje y ¡dale a todo trapo!',
      s_EN_YYC.translation_cz = 'Všichni makají na víkend, kámo! Přestaň dělat ramena bez výsledků, otevři vrata garáže a prostě to roztaj na plný plyn!',
      s_EN_YYC.translation_de = 'Alle arbeiten fürs Wochenende, Kumpel! Hör auf zu schauspielern, mach das Garagentor auf und gib einfach Vollgas!',
      s_EN_YYC.cultural_vibe = 'Mechanical momentum, straight-shooting energy, zero corporate polish';

// 5. SOTOGRANDE / ANDALUSIA (SPAIN): Camarón de la Isla - "Volando Voy"
MERGE (s_ES_SOT:Song {uid: 'SONG_ES_SOT_CAMARON'})
  SET s_ES_SOT.title = 'Volando Voy',
      s_ES_SOT.artist = 'Camarón de la Isla (Kiko Veneno)',
      s_ES_SOT.city_region = 'Sotogrande & Andalucian Coast',
      s_ES_SOT.genre = 'Flamenco-Rumba / Andaluz Moderno',
      s_ES_SOT.original_lyric = 'Volando voy, volando vengo, por el camino yo me entretengo. Enamorao de la vida, porque esto tiene duende y no hay que mirar los toros desde la barrera.',
      s_ES_SOT.original_lang = 'ES_SOT',
      s_ES_SOT.translation_en = 'Flying I go, flying I come, along the way I enjoy myself. In love with life, because this has true duende and you shouldn\'t watch the bulls from the sidelines.',
      s_ES_SOT.translation_cz = 'Létám sem a tam, cestou se bavím. Zamilovaný do života, bo to má skutočný duende a nemá smysl koukat na býky jen z bariéry.',
      s_ES_SOT.translation_de = 'Fliegend komme ich, fliegend gehe ich, unterwegs genieße ich das Leben. Verliebt ins Leben, weil das echten Duende hat und man nicht nur von der Tribüne zuschauen sollte.',
      s_ES_SOT.cultural_vibe = 'Sensory hyperbole, conspiratorial rhythm, unmanufacturable passion';

// 6. GLOBAL TRACK: The Weeknd ft. JENNIE & Lily-Rose Depp - "One of the Girls"
MERGE (s_WEEKND:Song {uid: 'SONG_WEEKND_OOTG'})
  SET s_WEEKND.title = 'One of the Girls',
      s_WEEKND.artist = 'The Weeknd, JENNIE, Lily-Rose Depp',
      s_WEEKND.city_region = 'Global / Nightlife High-Stakes Pop',
      s_WEEKND.genre = 'Nocturnal R&B / Dark Synthwave',
      s_WEEKND.original_lyric = 'Give me tough love, leave me with no breath... Push me down on my knees, tell me I belong to the world.',
      s_WEEKND.original_lang = 'EN',
      s_WEEKND.translation_es = 'Dame amor duro, déjame sin aliento... Empújame de rodillas, dime que pertenezco al mundo.',
      s_WEEKND.translation_cz = 'Dej mi tvrdou lásku, nech mě bez dechu... Sraz mě na kolena, řekni mi, že patřím světu.',
      s_WEEKND.translation_de = 'Gib mir harte Liebe, lass mich atemlos... Drück mich auf die Knie, sag mir, dass ich der Welt gehöre.',
      s_WEEKND.translation_ru = 'Дай мне суровую любовь, оставь меня без дыхания... Поставь меня на колени, скажи, что я принадлежу миру.',
      s_WEEKND.cultural_vibe = 'High-stakes nightlife intensity, intense devotion, chameleon surrender & velvet power dynamics';

// Connect Songs to Personas
MATCH (p:Persona {id: 'CZ_OVA'}), (s:Song {uid: 'SONG_CZ_OVA_NOHAVICA'}) MERGE (p)-[:HAS_REGIONAL_ANTHEM]->(s);
MATCH (p:Persona {id: 'AT_VIE'}), (s:Song {uid: 'SONG_AT_VIE_FALCO'}) MERGE (p)-[:HAS_REGIONAL_ANTHEM]->(s);
MATCH (p:Persona {id: 'RU_ALA'}), (s:Song {uid: 'SONG_RU_ALA_ASTUDIO'}) MERGE (p)-[:HAS_REGIONAL_ANTHEM]->(s);
MATCH (p:Persona {id: 'EN_YYC'}), (s:Song {uid: 'SONG_EN_YYC_LOVERBOY'}) MERGE (p)-[:HAS_REGIONAL_ANTHEM]->(s);
MATCH (p:Persona {id: 'ES_SOT'}), (s:Song {uid: 'SONG_ES_SOT_CAMARON'}) MERGE (p)-[:HAS_REGIONAL_ANTHEM]->(s);
MATCH (p:Persona {id: 'EN_YYC'}), (s:Song {uid: 'SONG_WEEKND_OOTG'}) MERGE (p)-[:HAS_REGIONAL_ANTHEM]->(s);

// ----------------------------------------------------------------------------
// 5. KEY VOCABULARY NODES (:Vocab) FROM IB PAST PAPERS & REGIONAL SOURCES
// ----------------------------------------------------------------------------

// --- CZECH VOCABULARY ---
MERGE (v_CZ_ZAMERIT:Vocab {uid: 'CZ_V_ZAMERIT'})
  SET v_CZ_ZAMERIT.term = 'zaměřit se na (+ Acc)',
      v_CZ_ZAMERIT.lang = 'CZ', v_CZ_ZAMERIT.register = 'FORMAL_EXAM',
      v_CZ_ZAMERIT.meaning = 'Focus on / target specifically',
      v_CZ_ZAMERIT.ib_source = 'Czech A1 Paper 1 HL/SL',
      v_CZ_ZAMERIT.grammar = 'German-calqued prepositional governance (fokussieren auf)';

MERGE (v_CZ_DATOVAL:Vocab {uid: 'CZ_V_DATOVAL'})
  SET v_CZ_DATOVAL.term = 'dávat si pozor na (+ Acc)',
      v_CZ_DATOVAL.lang = 'CZ', v_CZ_DATOVAL.register = 'FORMAL_EXAM',
      v_CZ_DATOVAL.meaning = 'Exercise caution / pay strict attention to',
      v_CZ_DATOVAL.ib_source = 'Czech B2B & Academic Outreach',
      v_CZ_DATOVAL.grammar = 'Mandatory Accusative governance';

MERGE (v_CZ_ROZBOR:Vocab {uid: 'CZ_V_ROZBOR'})
  SET v_CZ_ROZBOR.term = 'literární a strukturální rozbor',
      v_CZ_ROZBOR.lang = 'CZ', v_CZ_ROZBOR.register = 'FORMAL_EXAM',
      v_CZ_ROZBOR.meaning = 'Literary and structural breakdown',
      v_CZ_ROZBOR.ib_source = 'Czech A1 Paper 2 HL';

MERGE (v_CZ_FACHAT:Vocab {uid: 'CZ_V_FACHAT'})
  SET v_CZ_FACHAT.term = 'fachat',
      v_CZ_FACHAT.lang = 'CZ', v_CZ_FACHAT.register = 'REGIONAL_RIFF',
      v_CZ_FACHAT.meaning = 'Work / function reliably without friction',
      v_CZ_FACHAT.ib_source = 'Ostravština Dialect Study',
      v_CZ_FACHAT.etymology = 'Industrial Austrian loanword (fachen / arbeiten)';

MERGE (v_CZ_SICHTA:Vocab {uid: 'CZ_V_SICHTA'})
  SET v_CZ_SICHTA.term = 'šichta',
      v_CZ_SICHTA.lang = 'CZ', v_CZ_SICHTA.register = 'REGIONAL_RIFF',
      v_CZ_SICHTA.meaning = 'Heavy work shift / manual grind',
      v_CZ_SICHTA.ib_source = 'Ostravština Dialect Study',
      v_CZ_SICHTA.etymology = 'German Schicht';

MERGE (v_CZ_FAJRONT:Vocab {uid: 'CZ_V_FAJRONT'})
  SET v_CZ_FAJRONT.term = 'fajront',
      v_CZ_FAJRONT.lang = 'CZ', v_CZ_FAJRONT.register = 'REGIONAL_RIFF',
      v_CZ_FAJRONT.meaning = 'Quitting time / clean finish of work day',
      v_CZ_FAJRONT.ib_source = 'Ostravština Dialect Study',
      v_CZ_FAJRONT.etymology = 'German Feierabend';

MERGE (v_CZ_BO:Vocab {uid: 'CZ_V_BO'})
  SET v_CZ_BO.term = 'bo',
      v_CZ_BO.lang = 'CZ', v_CZ_BO.register = 'REGIONAL_RIFF',
      v_CZ_BO.meaning = 'Causal connector "because" (never "or")',
      v_CZ_BO.ib_source = 'Silesian & Northeast Czech Grammar',
      v_CZ_BO.etymology = 'Silesian contact particle';

// --- GERMAN VOCABULARY ---
MERGE (v_DE_ERORTERUNG:Vocab {uid: 'DE_V_ERORTERUNG'})
  SET v_DE_ERORTERUNG.term = 'die Erörterung',
      v_DE_ERORTERUNG.lang = 'DE', v_DE_ERORTERUNG.register = 'FORMAL_EXAM',
      v_DE_ERORTERUNG.meaning = 'Structured argumentative essay / text discussion',
      v_DE_ERORTERUNG.ib_source = 'German A Language & Literature Paper 1 HL';

MERGE (v_DE_STILMITTEL:Vocab {uid: 'DE_V_STILMITTEL'})
  SET v_DE_STILMITTEL.term = 'rhetorische Stilmittel',
      v_DE_STILMITTEL.lang = 'DE', v_DE_STILMITTEL.register = 'FORMAL_EXAM',
      v_DE_STILMITTEL.meaning = 'Rhetorical devices and stylistic techniques',
      v_DE_STILMITTEL.ib_source = 'German A2 Paper 1 HL';

MERGE (v_DE_AUSWIRKEN:Vocab {uid: 'DE_V_AUSWIRKEN'})
  SET v_DE_AUSWIRKEN.term = 'sich auswirken auf (+ Acc)',
      v_DE_AUSWIRKEN.lang = 'DE', v_DE_AUSWIRKEN.register = 'FORMAL_EXAM',
      v_DE_AUSWIRKEN.meaning = 'Exert an impact / influence upon',
      v_DE_AUSWIRKEN.ib_source = 'German Academic B2B';

MERGE (v_DE_SCHMAEH:Vocab {uid: 'DE_V_SCHMAEH'})
  SET v_DE_SCHMAEH.term = 'Wiener Schmäh',
      v_DE_SCHMAEH.lang = 'DE', v_DE_SCHMAEH.register = 'REGIONAL_RIFF',
      v_DE_SCHMAEH.meaning = 'Charming Viennese irony & status-equalizing wit',
      v_DE_SCHMAEH.ib_source = 'Wiener Schmäh Study';

MERGE (v_DE_PARTICLES:Vocab {uid: 'DE_V_PARTICLES'})
  SET v_DE_PARTICLES.term = 'eh / halt / ja / mal',
      v_DE_PARTICLES.lang = 'DE', v_DE_PARTICLES.register = 'REGIONAL_RIFF',
      v_DE_PARTICLES.meaning = 'Modal particles modulating speaker stance & rapport',
      v_DE_PARTICLES.ib_source = 'Subtle Art of German Modal Particles';

MERGE (v_DE_GSCHICHTL:Vocab {uid: 'DE_V_GSCHICHTL'})
  SET v_DE_GSCHICHTL.term = 'G’schichtldrucken',
      v_DE_GSCHICHTL.lang = 'DE', v_DE_GSCHICHTL.register = 'REGIONAL_RIFF',
      v_DE_GSCHICHTL.meaning = 'Tall-tale spinning / corporate puffery',
      v_DE_GSCHICHTL.ib_source = 'Austrian Conversational Register';

// --- RUSSIAN VOCABULARY ---
MERGE (v_RU_ANALIZ:Vocab {uid: 'RU_V_ANALIZ'})
  SET v_RU_ANALIZ.term = 'сопоставительный анализ',
      v_RU_ANALIZ.lang = 'RU', v_RU_ANALIZ.register = 'FORMAL_EXAM',
      v_RU_ANALIZ.meaning = 'Comparative literary breakdown',
      v_RU_ANALIZ.ib_source = 'Russian A1 Paper 1 HL/SL';

MERGE (v_RU_SREDSTVA:Vocab {uid: 'RU_V_SREDSTVA'})
  SET v_RU_SREDSTVA.term = 'изобразительно-выразительные средства',
      v_RU_SREDSTVA.lang = 'RU', v_RU_SREDSTVA.register = 'FORMAL_EXAM',
      v_RU_SREDSTVA.meaning = 'Expressive and poetic devices',
      v_RU_SREDSTVA.ib_source = 'Russian A1 Paper 2 HL';

MERGE (v_RU_OPIRATSA:Vocab {uid: 'RU_V_OPIRATSA'})
  SET v_RU_OPIRATSA.term = 'опираться на (+ Acc)',
      v_RU_OPIRATSA.lang = 'RU', v_RU_OPIRATSA.register = 'FORMAL_EXAM',
      v_RU_OPIRATSA.meaning = 'Rely upon / base arguments on',
      v_RU_OPIRATSA.ib_source = 'Russian B Paper 2 SL';

MERGE (v_RU_KRASOTA:Vocab {uid: 'RU_V_KRASOTA'})
  SET v_RU_KRASOTA.term = 'сделали по красоте',
      v_RU_KRASOTA.lang = 'RU', v_RU_KRASOTA.register = 'REGIONAL_RIFF',
      v_RU_KRASOTA.meaning = 'Executed flawlessly with aesthetic mastery',
      v_RU_KRASOTA.ib_source = 'Almaty Working Register';

MERGE (v_RU_BAZARU:Vocab {uid: 'RU_V_BAZARU'})
  SET v_RU_BAZARU.term = 'базару нет',
      v_RU_BAZARU.lang = 'RU', v_RU_BAZARU.register = 'REGIONAL_RIFF',
      v_RU_BAZARU.meaning = 'Unquestionably / zero doubt',
      v_RU_BAZARU.ib_source = 'Almaty Working Register';

// --- ENGLISH VOCABULARY ---
MERGE (v_EN_RHETORIC:Vocab {uid: 'EN_V_RHETORIC'})
  SET v_EN_RHETORIC.term = 'rhetorical appeal & authorial choice',
      v_EN_RHETORIC.lang = 'EN', v_EN_RHETORIC.register = 'FORMAL_EXAM',
      v_EN_RHETORIC.meaning = 'Persuasive strategy and stylistic decisions',
      v_EN_RHETORIC.ib_source = 'English A Language & Literature Paper 1 SL';

MERGE (v_EN_HINGE:Vocab {uid: 'EN_V_HINGE'})
  SET v_EN_HINGE.term = 'hinge upon (+ Noun)',
      v_EN_HINGE.lang = 'EN', v_EN_HINGE.register = 'FORMAL_EXAM',
      v_EN_HINGE.meaning = 'Depend fundamentally on a pivotal condition',
      v_EN_HINGE.ib_source = 'English B Paper 2 HL';

MERGE (v_EN_CATTLE:Vocab {uid: 'EN_V_CATTLE'})
  SET v_EN_CATTLE.term = 'all hat and no cattle',
      v_EN_CATTLE.lang = 'EN', v_EN_CATTLE.register = 'REGIONAL_RIFF',
      v_EN_CATTLE.meaning = 'All talk and posture without underlying substance',
      v_EN_CATTLE.ib_source = 'Calgary Foothills Register';

MERGE (v_EN_GIVE_ER:Vocab {uid: 'EN_V_GIVE_ER'})
  SET v_EN_GIVE_ER.term = 'give ’er',
      v_EN_GIVE_ER.lang = 'EN', v_EN_GIVE_ER.register = 'REGIONAL_RIFF',
      v_EN_GIVE_ER.meaning = 'Go all out / execute at full throttle',
      v_EN_GIVE_ER.ib_source = 'Calgary Foothills Register';

MERGE (v_EN_TOUGH_LOVE:Vocab {uid: 'EN_V_TOUGH_LOVE'})
  SET v_EN_TOUGH_LOVE.term = 'tough love & high-stakes surrender',
      v_EN_TOUGH_LOVE.lang = 'EN', v_EN_TOUGH_LOVE.register = 'REGIONAL_RIFF',
      v_EN_TOUGH_LOVE.meaning = 'Uncompromising emotional intensity and velvet submission to the flow',
      v_EN_TOUGH_LOVE.ib_source = 'The Weeknd - One of the Girls';

// --- SPANISH VOCABULARY ---
MERGE (v_ES_ANALISIS:Vocab {uid: 'ES_V_ANALISIS'})
  SET v_ES_ANALISIS.term = 'análisis de recursos estilísticos',
      v_ES_ANALISIS.lang = 'ES', v_ES_ANALISIS.register = 'FORMAL_EXAM',
      v_ES_ANALISIS.meaning = 'Analysis of literary and stylistic resources',
      v_ES_ANALISIS.ib_source = 'Spanish A1 Paper 1 HL';

MERGE (v_ES_MANIFIESTO:Vocab {uid: 'ES_V_MANIFIESTO'})
  SET v_ES_MANIFIESTO.term = 'poner de manifiesto',
      v_ES_MANIFIESTO.lang = 'ES', v_ES_MANIFIESTO.register = 'FORMAL_EXAM',
      v_ES_MANIFIESTO.meaning = 'Highlight / demonstrate explicitly',
      v_ES_MANIFIESTO.ib_source = 'Spanish ab initio Paper 1 SL';

MERGE (v_ES_DUENDE:Vocab {uid: 'ES_V_DUENDE'})
  SET v_ES_DUENDE.term = 'tener duende',
      v_ES_DUENDE.lang = 'ES', v_ES_DUENDE.register = 'REGIONAL_RIFF',
      v_ES_DUENDE.meaning = 'Possess unmanufacturable soul and magnetic presence',
      v_ES_DUENDE.ib_source = 'Sotogrande Andaluz Register';

MERGE (v_ES_TOROS:Vocab {uid: 'ES_V_TOROS'})
  SET v_ES_TOROS.term = 'mirar los toros desde la barrera',
      v_ES_TOROS.lang = 'ES', v_ES_TOROS.register = 'REGIONAL_RIFF',
      v_ES_TOROS.meaning = 'Observe passively from safety without taking risk',
      v_ES_TOROS.ib_source = 'Sotogrande Andaluz Register';

// Connect Songs to Vocabulary Slang Nodes
MATCH (s:Song {uid: 'SONG_CZ_OVA_NOHAVICA'}), (v1:Vocab {uid: 'CZ_V_SICHTA'}), (v2:Vocab {uid: 'CZ_V_FAJRONT'}), (v3:Vocab {uid: 'CZ_V_BO'})
  MERGE (s)-[:INJECTS_SLANG]->(v1) MERGE (s)-[:INJECTS_SLANG]->(v2) MERGE (s)-[:INJECTS_SLANG]->(v3);

MATCH (s:Song {uid: 'SONG_AT_VIE_FALCO'}), (v1:Vocab {uid: 'DE_V_SCHMAEH'}), (v2:Vocab {uid: 'DE_V_PARTICLES'})
  MERGE (s)-[:INJECTS_SLANG]->(v1) MERGE (s)-[:INJECTS_SLANG]->(v2);

MATCH (s:Song {uid: 'SONG_RU_ALA_ASTUDIO'}), (v1:Vocab {uid: 'RU_V_KRASOTA'}), (v2:Vocab {uid: 'RU_V_BAZARU'})
  MERGE (s)-[:INJECTS_SLANG]->(v1) MERGE (s)-[:INJECTS_SLANG]->(v2);

MATCH (s:Song {uid: 'SONG_EN_YYC_LOVERBOY'}), (v1:Vocab {uid: 'EN_V_CATTLE'}), (v2:Vocab {uid: 'EN_V_GIVE_ER'})
  MERGE (s)-[:INJECTS_SLANG]->(v1) MERGE (s)-[:INJECTS_SLANG]->(v2);

MATCH (s:Song {uid: 'SONG_ES_SOT_CAMARON'}), (v1:Vocab {uid: 'ES_V_DUENDE'}), (v2:Vocab {uid: 'ES_V_TOROS'})
  MERGE (s)-[:INJECTS_SLANG]->(v1) MERGE (s)-[:INJECTS_SLANG]->(v2);

MATCH (s:Song {uid: 'SONG_WEEKND_OOTG'}), (v:Vocab {uid: 'EN_V_TOUGH_LOVE'})
  MERGE (s)-[:INJECTS_SLANG]->(v);

// ----------------------------------------------------------------------------
// 6. SEED 4-C FORMAL EXECUTIVE & LYRIC-INFUSED CARDS (:Card)
// ----------------------------------------------------------------------------
MERGE (c_CZ_EXEC_COMP:Card {uid: 'CZ_EXEC_COMP'})
  SET c_CZ_EXEC_COMP.lang = 'CZ_FORMAL', c_CZ_EXEC_COMP.stage = 'COMPLIMENT',
      c_CZ_EXEC_COMP.text = 'Vážený pane architekte, sleduji přesnost vašich projektů a oceňuji, jak čistě držite strukturální rozbor bez zbytečného šumu.';

MERGE (c_CZ_EXEC_CHAM:Card {uid: 'CZ_EXEC_CHAM'})
  SET c_CZ_EXEC_CHAM.lang = 'CZ_FORMAL', c_CZ_EXEC_CHAM.stage = 'CHAMELEON',
      c_CZ_EXEC_CHAM.text = 'Ve V3DV se zaměřujeme přesně na tyto oblasti – stavíme modulární AI nadstavbu tak, abychom do firmy nevnášeli další zbytečný software.';

MERGE (c_CZ_EXEC_COUNT:Card {uid: 'CZ_EXEC_COUNT'})
  SET c_CZ_EXEC_COUNT.lang = 'CZ_FORMAL', c_CZ_EXEC_COUNT.stage = 'COUNTERACT',
      c_CZ_EXEC_COUNT.text = 'Při tomto tempu škálování je však spoléhat se na manuální předávání dat rizikem, které zbytečně prodlužuje schvalovací cyklus.';

MERGE (c_CZ_EXEC_CUR:Card {uid: 'CZ_EXEC_CUR'})
  SET c_CZ_EXEC_CUR.lang = 'CZ_FORMAL', c_CZ_EXEC_CUR.stage = 'CURIOSITY',
      c_CZ_EXEC_CUR.text = 'Máte příští týden v úterý nebo ve čtvrtek 15 minut na krátký hovor, kde bychom prošli, jak tuto architekturu nasadit přímo u vás?';

// Connect Songs to 4-C Cards (Cultural Anthem Reinforcement)
MATCH (s:Song {uid: 'SONG_CZ_OVA_NOHAVICA'}), (c:Card {uid: 'CZ_OVA_COUNT'}) MERGE (s)-[:REINFORCES_CARD_VIBE]->(c);
MATCH (s:Song {uid: 'SONG_AT_VIE_FALCO'}), (c:Card {uid: 'AT_VIE_CHAM'}) MERGE (s)-[:REINFORCES_CARD_VIBE]->(c);
MATCH (s:Song {uid: 'SONG_RU_ALA_ASTUDIO'}), (c:Card {uid: 'RU_ALA_COMP'}) MERGE (s)-[:REINFORCES_CARD_VIBE]->(c);
MATCH (s:Song {uid: 'SONG_EN_YYC_LOVERBOY'}), (c:Card {uid: 'EN_YYC_CUR'}) MERGE (s)-[:REINFORCES_CARD_VIBE]->(c);
MATCH (s:Song {uid: 'SONG_ES_SOT_CAMARON'}), (c:Card {uid: 'ES_SOT_COMP'}) MERGE (s)-[:REINFORCES_CARD_VIBE]->(c);
MATCH (s:Song {uid: 'SONG_WEEKND_OOTG'}), (c:Card {uid: 'EN_YYC_CHAM'}) MERGE (s)-[:REINFORCES_CARD_VIBE]->(c);

// ----------------------------------------------------------------------------
// 7. CROSS-REGISTER CODE-SWITCH BRIDGES & TRANSITION PATHS
// ----------------------------------------------------------------------------
// Bridge: Executive Czech Formal -> Ostravian Working Riff
MERGE (b_CZ_FORMAL_TO_OVA:Bridge {uid: 'BRIDGE_CZ_FORMAL_TO_OVA'})
  SET b_CZ_FORMAL_TO_OVA.from_lang = 'CZ_FORMAL', b_CZ_FORMAL_TO_OVA.to_lang = 'CZ_OVA',
      b_CZ_FORMAL_TO_OVA.text = 'Ale když se na to podíváme pod kapotou...',
      b_CZ_FORMAL_TO_OVA.transition_type = 'FORMAL_TO_REGIONAL_PIVOT';

MATCH (c1:Card {uid: 'CZ_EXEC_CHAM'}), (b:Bridge {uid: 'BRIDGE_CZ_FORMAL_TO_OVA'}), (c2:Card {uid: 'CZ_OVA_COUNT'})
  MERGE (c1)-[:PIVOTS_VIA {weight: 0.82, days_ago: 1, drills: 6}]->(b)
  MERGE (b)-[:LANDS_ON]->(c2);

// Bridge: Hochdeutsch Formal -> Wiener Schmäh
MERGE (b_DE_FORMAL_TO_VIE:Bridge {uid: 'BRIDGE_DE_FORMAL_TO_VIE'})
  SET b_DE_FORMAL_TO_VIE.from_lang = 'DE_FORMAL', b_DE_FORMAL_TO_VIE.to_lang = 'AT_VIE',
      b_DE_FORMAL_TO_VIE.text = 'Wenn wir aber ehrlich sind...',
      b_DE_FORMAL_TO_VIE.transition_type = 'FORMAL_TO_REGIONAL_PIVOT';

// ----------------------------------------------------------------------------
// 8. FALSE-FRIEND SAFETY ALERTS (SLAVIC & GERMANIC INTERFERENCE)
// ----------------------------------------------------------------------------
MERGE (ff_uzasny:Vocab {uid: 'FF_CZ_UZASNY'})
  SET ff_uzasny.term = 'Úžasný (CZ) vs Ужасный (RU)',
      ff_uzasny.warning = 'CRITICAL FALSE FRIEND: Czech "úžasný" means amazing/wonderful, whereas Russian "ужасный" means terrible/horrible.';

MERGE (ff_cerstvy:Vocab {uid: 'FF_CZ_CERSTVY'})
  SET ff_cerstvy.term = 'Čerstvý (CZ) vs Черствый (RU)',
      ff_cerstvy.warning = 'CRITICAL FALSE FRIEND: Czech "čerstvý" means fresh (e.g. čerstvá data), whereas Russian "черствый" means stale/hard bread.';

MERGE (ff_pozor:Vocab {uid: 'FF_CZ_POZOR'})
  SET ff_pozor.term = 'Pozor! (CZ) vs Позор (RU)',
      ff_pozor.warning = 'CRITICAL FALSE FRIEND: Czech "Dávat si pozor" means to exercise care/attention, whereas Russian "позор" means shame/disgrace.';

MATCH (v1:Vocab {uid: 'CZ_V_ZAMERIT'}), (ff:Vocab {uid: 'FF_CZ_POZOR'})
  MERGE (v1)-[:FALSE_FRIEND_ALERT]->(ff);

// ----------------------------------------------------------------------------
// 9. SRS EDGE MASTERY TELEMETRY (SAMPLE FLOWS & WEIGHTS)
// ----------------------------------------------------------------------------
MATCH (a:Card {uid: 'CZ_EXEC_COMP'}), (b:Card {uid: 'CZ_EXEC_CHAM'})
  MERGE (a)-[r:FLOWS_TO]->(b) SET r.weight = 0.91, r.days_ago = 1, r.drills = 7;

MATCH (a:Card {uid: 'CZ_EXEC_CHAM'}), (b:Card {uid: 'CZ_EXEC_COUNT'})
  MERGE (a)-[r:FLOWS_TO]->(b) SET r.weight = 0.85, r.days_ago = 2, r.drills = 6;

MATCH (a:Card {uid: 'CZ_EXEC_COUNT'}), (b:Card {uid: 'CZ_EXEC_CUR'})
  MERGE (a)-[r:FLOWS_TO]->(b) SET r.weight = 0.78, r.days_ago = 3, r.drills = 5;
