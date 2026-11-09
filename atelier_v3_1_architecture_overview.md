# Polyglot Interpersonal Riff Studio & Neo4j SRS Engine v3.1 (Atelier Edition)

The **Polyglot Interpersonal Riff Studio & Neo4j SRS Engine v3.1** combines a 5-persona linguistic matrix (`CZ_OVA`, `AT_VIE`, `RU_ALA`, `EN_YYC`, `ES_SOT`) with a stateful property graph that tracks conversational transitions, etymological roots, spaced-repetition (SRS) mastery, and live room-friction objection resolution.

## Atelier v3.1 Architecture Overview

```text
+---------------------------------------------------------------------------------------------------+
|                             1. REGIONAL PERSONA & REGISTER MATRIX                                 |
+-------------------+-------------------+-------------------+-------------------+-------------------+
|  🇨🇿 CZ_OVA        |    🇦🇹 AT_VIE      |    🇰🇿 RU_ALA      |    🇨🇦 EN_YYC      |    🇪🇸 ES_SOT      |
|   Ostravština &   |   Wiener Schmäh   |  Almaty Insider   |   Calgary Flair   | Sotogrande Duende |
| Industrial Peer   | Kaffeehaus Irony  |  Terrace Candor   | Backstage Punch   |  Andaluz Rhythm   |
+---------+---------+---------+---------+---------+---------+---------+---------+---------+---------+
          |                   |                   |                   |                   |
          +-------------------+-------------------+-------------------+-------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|                        2. CONVERSATIONAL GRAPH TOPOLOGY (THE 4 Cs ENGINE)                         |
|                                                                                                   |
|   [ 1. COMPLIMENT ] ===(:FLOWS_TO {w, drills})===> [ 2. CHAMELEON ]                               |
|     Spotlights craft                                 Matches phonetic &                           |
|     & real execution                                 grammatical rhythm                           |
|                                                             |                                     |
|                      +-------(:PIVOTS_VIA {weight})---------+                                     |
|                      |                                      |                                     |
|                      v                                      v                                     |
|             ( :Bridge Node )                        (:FLOWS_TO {w})                               |
|          Mid-sentence code-switch                           |                                     |
|          or C-Suite -> Dev drop                             |                                     |
|                      |                                      |                                     |
|                      +------------(:LANDS_ON)---------------+                                     |
|                                                             v                                     |
|   [ 4. CURIOSITY ] <===(:FLOWS_TO {w, drills})==== [ 3. COUNTERACT ] <---(:COUNTERS_STATE)--- [State]|
|     Open-loop hook                                   Velvet pushback &              Objection     |
|     stripping friction                               half-octave drop               Resolver      |
+---------------------------------------------------------------------------------------------------+
```

