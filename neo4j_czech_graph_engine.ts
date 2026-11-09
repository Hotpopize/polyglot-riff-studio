import neo4j, { Driver, Session } from 'neo4j-driver';

export class CzechGraphEngine {
  private driver: Driver;

  constructor(uri: string, user: string, pass: string) {
    this.driver = neo4j.driver(uri, neo4j.auth.basic(user, pass));
  }

  /**
   * Traveses the graph from Executive Standard Czech down to Ostravian Engineering peer talk
   */
  async getCzechRegisterDropChain(targetVibe: string): Promise<any> {
    const session: Session = this.driver.session();
    const query = `
      MATCH path = (c1:Card {lang: 'CZ_STD', stage: 'COMPLIMENT'})
        -[:FLOWS_TO|PIVOTS_VIA|LANDS_ON*1..4]->
        (cEnd:Card {lang: 'CZ_OVA'})
      WHERE c1.vibe = $vibe
      RETURN nodes(path) AS chain, relationships(path) AS transitions
    `;

    try {
      const result = await session.run(query, { vibe: targetVibe });
      return result.records.map(record => ({
        nodes: record.get('chain').map((n: any) => n.properties),
        transitions: record.get('transitions').map((r: any) => r.type)
      }));
    } finally {
      await session.close();
    }
  }

  /**
   * Updates edge weight based on user practice performance (Spaced Repetition feedback)
   */
  async updateTraversalWeight(fromUid: string, toUid: string, score: number): Promise<void> {
    const session: Session = this.driver.session();
    const query = `
      MATCH (a:Card {uid: $fromUid})-[r:FLOWS_TO|PIVOTS_VIA]->(b:Card {uid: $toUid})
      SET r.weight = apoc.math.clamp(r.weight * (1.0 + ($score - 3) * 0.1), 0.1, 1.0),
          r.last_drilled = timestamp()
    `;
    try {
      await session.run(query, { fromUid, toUid, score });
    } finally {
      await session.close();
    }
  }
}