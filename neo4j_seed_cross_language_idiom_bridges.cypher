// Wire cross-language etymological & conceptual bridges between Idiom nodes
MATCH (iOva:Idiom {term: 'fajront'}), (iVie:Idiom {term: 'an der Garderobe abgeben'})
MERGE (iOva)-[:SHARES_VIBE_WITH {
  shared_root: 'Austro-Hungarian Industrial / Kaffeehaus Boundary',
  pivot_tip: 'Use the exact same downward vocal exhale on both phrases to signal "work is over, now we talk like humans."'
}]->(iVie);

MATCH (iOva2:Idiom {term: 'fachat'}), (iAla:Idiom {term: 'сделали по красоте'})
MERGE (iOva2)-[:SHARES_VIBE_WITH {
  shared_root: 'High-Craft Execution',
  pivot_tip: 'Both carry grounded engineering respect—drop corporate adjectives and let the verb carry the weight.'
}]->(iAla);