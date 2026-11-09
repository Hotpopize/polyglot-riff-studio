// Upgraded FSRS-Lite Retrievability & Stability Engine
function computeRetrievability(edge) {
  const stability = edge.stability || (edge.drills || 1) * 3.5; // Stability S in days
  const days = edge.daysAgo || 0;
  // Exponential forgetting curve: R(t) = (1 + t / (9 * S))^-1
  return +(Math.pow(1 + days / (9 * stability), -1)).toFixed(2);
}

function isEdgeRusty(edge) {
  const R = computeRetrievability(edge);
  return R < 0.75 || edge.weight < 0.60;
}

function gradeActiveTransitionFSRS(score) {
  const edge = state.edges.find(e => e.id === state.selectedEdgeId);
  if (!edge) return;

  const prevStability = edge.stability || 4.0;
  // Score: 1 (Rusty/Reset), 3 (Solid), 5 (Nailed It)
  if (score === 1) {
    edge.stability = Math.max(1.5, +(prevStability * 0.45).toFixed(2));
    edge.weight = Math.max(0.20, +(edge.weight - 0.15).toFixed(2));
  } else {
    const multiplier = score === 5 ? 1.85 : 1.25;
    edge.stability = +(prevStability * multiplier).toFixed(2);
    edge.weight = Math.min(0.99, +(edge.weight + (score - 3) * 0.07 + 0.03).toFixed(2));
    edge.daysAgo = 0;
  }
  edge.drills = (edge.drills || 1) + 1;
  saveState();
  renderCards();
}