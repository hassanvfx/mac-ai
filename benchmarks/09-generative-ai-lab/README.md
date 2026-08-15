# Generative AI Lab — Case-Study Evidence Record

**Recorded:** 2026-08-15  
**Scope:** Documentation-led architecture and safety review; not a performance benchmark.

## Sources inspected

- Lyrics Refiner: <https://github.com/hassanvfx/lyrics-refiner>
- Lyrics Refiner engineering article: <https://uriostegui.medium.com/turn-raw-lyrics-into-performance-ready-songs-92f62322ff9e?postPublishedType=initial>
- Newsmusic: <https://github.com/hassanvfx/newsmusic>
- Newsmusic project story: <https://uriostegui.medium.com/75427bae1309>

## Recorded observations

| Case study | Declared source boundary | Check or approval boundary | Safe-first mode |
| --- | --- | --- | --- |
| Lyrics Refiner | Writer-owned lyrics; local user-owned API key | Deterministic source-word preservation report; writer reviews export | Local setup only; no deployed build with a browser-exposed key |
| Newsmusic | Configured news metadata/transcripts; creator-owned credentials | Dry-run path; private, review-gated delivery; human factual/rights review | `orchestrate --until video --dry-run` |

## Non-claims

This record reports documented workflow boundaries only. It does not measure
model quality, latency, cost, audience growth, monetization, legal clearance,
or platform-policy compliance. External repositories evolve independently; read
their current documentation before running them.
