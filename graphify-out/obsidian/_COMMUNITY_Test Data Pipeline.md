---
type: community
cohesion: 0.24
members: 11
---

# Test Data Pipeline

**Cohesion:** 0.24 - loosely connected
**Members:** 11 nodes

## Members
- [[Schéma otázky (q, opts, correct)]] - document - docs/pridat-test.md
- [[Schéma souboru testu (id, title, updatedAt, rubric, questions)]] - document - docs/pridat-test.md
- [[TESTS_REGISTRY — registr testů]] - code - index.html
- [[Test Komunikace a komunikační dovednosti (103 otázek)]] - code - index.html
- [[Test Management (86 otázek)]] - code - index.html
- [[Test Management starší verze (14 otázek)]] - code - index.html
- [[docspridat-test.md — návod na přidání nového testu]] - document - docs/pridat-test.md
- [[loadRegistry() — inicializace dashboardu]] - code - index.html
- [[renderDashboard() — vykreslení karet testů]] - code - index.html
- [[screen-start — obrazovka nastavení kvízu]] - code - index.html
- [[selectTest(id) — načtení JSON testu přes fetch]] - code - index.html

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Test_Data_Pipeline
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_App Infrastructure & Versioning]]
- 1 edge to [[_COMMUNITY_Quiz Core Functions]]
- 1 edge to [[_COMMUNITY_Management Knowledge Bank]]

## Top bridge nodes
- [[docspridat-test.md — návod na přidání nového testu]] - degree 6, connects to 1 community
- [[selectTest(id) — načtení JSON testu přes fetch]] - degree 4, connects to 1 community
- [[Test Management (86 otázek)]] - degree 2, connects to 1 community