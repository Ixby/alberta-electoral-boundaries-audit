// Alberta Electoral Boundary Audit — engine string table
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
//
// The map engine is framework-free vanilla TS and can't reach the Svelte
// i18n store. Instead, the host page injects translated strings through
// setEngineStrings() at init time and again on every language switch.
// English defaults below guarantee the engine renders sensibly even if
// the host forgets to inject.

export type EngineStrings = {
  votesSuffix: string;          // "11,518 votes"
  totalVotesSuffix: string;     // "16,268 total votes"
  popPrefix: string;            // "Pop. 48,200"
  votingAreasSuffix: string;    // "37 voting areas"
  otherMaps: string;            // compare-block header
  uniqueBoundary: string;       // compare-block fallback
  inPersonVotes: string;        // VA callout total line
  loadErrorGeneric: string;     // svgLoader failure
  loadErrorMap: string;         // maps.ts per-map failure; {key} placeholder
  contextMinority: string;      // ED callout context line per map
  contextMajority: string;
  context2019: string;
  tagMin: string;               // search-result map tags
  tagMaj: string;
  tag2019: string;
};

export const STR: EngineStrings = {
  votesSuffix: 'votes',
  totalVotesSuffix: 'total votes',
  popPrefix: 'Pop.',
  votingAreasSuffix: 'voting areas',
  otherMaps: 'Other maps',
  uniqueBoundary: 'Boundary unique to this map',
  inPersonVotes: 'in-person votes (excl. Vote Anywhere)',
  loadErrorGeneric: 'Could not load the boundary map. Try reloading the page.',
  loadErrorMap: 'Could not load the {key} map — check your connection.',
  contextMinority: '2026 minority proposal · 2023 election results',
  contextMajority: '2026 majority proposal · 2023 election results',
  context2019: '2019 enacted boundaries · 2023 election results',
  tagMin: 'Min',
  tagMaj: 'Maj',
  tag2019: '2019',
};

export function setEngineStrings(next: Partial<EngineStrings>): void {
  Object.assign(STR, next);
}
