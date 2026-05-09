# Graph Report - /Users/tomek/bananovnik  (2026-05-09)

## Corpus Check
- 17 files · ~71,979 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 129 nodes · 160 edges · 15 communities detected
- Extraction: 78% EXTRACTED · 22% INFERRED · 0% AMBIGUOUS · INFERRED: 35 edges (avg confidence: 0.85)
- Token cost: 1,712 input · 730 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Quiz Core Functions|Quiz Core Functions]]
- [[_COMMUNITY_Management Knowledge Bank|Management Knowledge Bank]]
- [[_COMMUNITY_App Icon Assets & Brand|App Icon Assets & Brand]]
- [[_COMMUNITY_Dazzle Icon Design|Dazzle Icon Design]]
- [[_COMMUNITY_Icon Shape & Color Variants|Icon Shape & Color Variants]]
- [[_COMMUNITY_Test Data Pipeline|Test Data Pipeline]]
- [[_COMMUNITY_App Infrastructure & Versioning|App Infrastructure & Versioning]]
- [[_COMMUNITY_Green Icon Variant|Green Icon Variant]]
- [[_COMMUNITY_Dazzle Style Visual Language|Dazzle Style Visual Language]]
- [[_COMMUNITY_Large Icon (1024px)|Large Icon (1024px)]]
- [[_COMMUNITY_Project Setup & Docs|Project Setup & Docs]]
- [[_COMMUNITY_Apple Touch Icon (180px)|Apple Touch Icon (180px)]]
- [[_COMMUNITY_Service Worker|Service Worker]]
- [[_COMMUNITY_Dashboard Screen|Dashboard Screen]]
- [[_COMMUNITY_Splash Screen|Splash Screen]]

## God Nodes (most connected - your core abstractions)
1. `Management EZK, Bc — banka testových otázek (primat.cz)` - 17 edges
2. `Banana Icon` - 10 edges
3. `S — stav běžícího kvízu (questions, cur, answers, scores, confirmed, retried)` - 9 edges
4. `App Icon: Banana — Dazzle Clean style (variant 3)` - 9 edges
5. `Banana Illustration (two bananas, yellow with dark red outline)` - 7 edges
6. `App Icon — Yellow Banana (Variant 4)` - 7 edges
7. `TESTS_REGISTRY — registr testů` - 6 edges
8. `renderQ() — vykreslení aktuální otázky a možností` - 6 edges
9. `docs/pridat-test.md — návod na přidání nového testu` - 6 edges
10. `App Icon Variant 2 — Green` - 6 edges

## Surprising Connections (you probably didn't know these)
- `Management EZK, Bc — banka testových otázek (primat.cz)` --conceptually_related_to--> `Test: Management (86 otázek)`  [INFERRED]
  docs/primat-Management EZK, Bc.pdf → index.html
- `Banana Illustration (two bananas, yellow with dark red outline)` --PRIMARY_COLOR--> `Yellow (#f0d540)`  [EXTRACTED]
  icons/5-dashboard.png → favicon.svg
- `favicon.svg — banánová ikona` --conceptually_related_to--> `Banánová SVG (An Nguyen, CC Attribution, SVG Repo)`  [INFERRED]
  index.html → icon-single.html
- `icon-generator.html — 5 variant ikon (krémová, zelená, dazzle, žlutá, mark)` --conceptually_related_to--> `favicon.svg — banánová ikona`  [INFERRED]
  icon-generator.html → index.html
- `docs/pridat-test.md — návod na přidání nového testu` --references--> `sw.js — Service Worker (offline cache)`  [EXTRACTED]
  docs/pridat-test.md → index.html

## Hyperedges (group relationships)
- **Hlavní tok kvízu: startQuiz → renderQ → mainBtn → showResults** — index_fn_start_quiz, index_fn_render_q, index_fn_main_btn, index_fn_show_results [EXTRACTED 0.95]
- **Pipeline testových dat: TESTS_REGISTRY → selectTest → S (stav kvízu)** — index_tests_registry, index_fn_select_test, index_state_s [EXTRACTED 0.92]
- **Konzistence verzí: sw.js + APP_VERSION + manifest.json?v= + version.json musí být synchronní** — index_sw_js, index_manifest_json, docs_version_bump, docs_rationale_version_bump [EXTRACTED 0.93]

## Communities

### Community 0 - "Quiz Core Functions"
Cohesion: 0.14
Nodes (19): bananaConfetti() / spawnBurst() — animace banánů při úspěchu, cfg — konfigurace kvízu (mode, count, fb, qorder, oorder, study), mainBtn() — potvrzení odpovědi nebo přechod na další otázku, openReview() — zobrazení přehledu odpovědí, renderQ() — vykreslení aktuální otázky a možností, retryQ() — opakování jednotlivé otázky (přeskládání možností), retryWrong() — opakování chybně zodpovězených otázek, setCount(n) — nastavení počtu otázek (+11 more)

### Community 1 - "Management Knowledge Bank"
Cohesion: 0.15
Nodes (17): Management EZK, Bc — banka testových otázek (primat.cz), Americký proud klasické školy managementu — efektivita dělníků, úkolová mzda, řízení a plánování výroby, Centralizace rozhodování — pravomoce soustředěny na vyšší manažery, Dobře strukturované problémy — časté, rychlé řešení, obvyklá znalost proměnných, opakování, Metody identifikace problému (kauzální analýza, šestislovný graf, graf příčin a následků), Funkce kontrolní činnosti (inspekční, eliminační, preventivní), Matematické modely pro podporu rozhodování (lineární optimalizační modely, rozhodovací modely, distribuční úlohy), Pojem organizace — označení pro firmy/úřady + trvalé uspořádání prvků a vazeb (+9 more)

### Community 2 - "App Icon Assets & Brand"
Cohesion: 0.15
Nodes (13): 512x512 App Icon, Banana Icon, Bananovnik App, CC Attribution License, Dark Red / Brown (#6f0911), Green (#4aa86a), White (#ffffff), Yellow (#f0d540) (+5 more)

### Community 3 - "Dazzle Icon Design"
Cohesion: 0.2
Nodes (15): Cream/pale yellow background color, Dark red / maroon outline color, Green stem accent color, White highlight / gloss on banana, Design label: Krémová + dazzle offset (variant 3), App Icon: Banana — Dazzle Clean style (variant 3), App Icon — Yellow Banana (Variant 4), Bananovnik app project (+7 more)

### Community 4 - "Icon Shape & Color Variants"
Cohesion: 0.24
Nodes (12): Rounded Square App Icon Shape, Banana Illustration (two bananas, yellow with dark red outline), Bananovnik Project, Beige / Sand (background color), Dark Red / Maroon (outline color), Cream / light yellow background color, Cream App Icon — banana illustration on cream/light-yellow rounded square background, Dashboard Style App Icon (logo-mark) (+4 more)

### Community 5 - "Test Data Pipeline"
Cohesion: 0.24
Nodes (11): docs/pridat-test.md — návod na přidání nového testu, Schéma otázky (q, opts[], correct[]), Schéma souboru testu (id, title, updatedAt, rubric, questions[]), loadRegistry() — inicializace dashboardu, renderDashboard() — vykreslení karet testů, selectTest(id) — načtení JSON testu přes fetch, screen-start — obrazovka nastavení kvízu, Test: Komunikace a komunikační dovednosti (103 otázek) (+3 more)

### Community 6 - "App Infrastructure & Versioning"
Cohesion: 0.31
Nodes (9): Rationale: SW cachuje seznam testů — bez bumpu verze uvidí uživatelé stará data, Postup bumpu verze (sw.js, APP_VERSION, manifest.json?v=, version.json), Banánová SVG (An Nguyen, CC Attribution, SVG Repo), icon-generator.html — 5 variant ikon (krémová, zelená, dazzle, žlutá, mark), icon-single.html — žlutá verze banánové ikony (1024×1024), Banánovník — hlavní aplikace (index.html), favicon.svg — banánová ikona, manifest.json — PWA manifest (+1 more)

### Community 7 - "Green Icon Variant"
Cohesion: 0.25
Nodes (9): Banana Illustration, Dark Red Outline Color, Green Background Color, Yellow Banana Color, App Icon Variant 2 — Green, Label: Zelená (Czech for Green), Cartoon / Comic Style, Rounded Square Shape (+1 more)

### Community 8 - "Dazzle Style Visual Language"
Cohesion: 0.53
Nodes (6): Banana Motif, Dark Red / Maroon Outline, Dazzle Icon Variant — Banana App Icon, Dazzle Design Style, Kremova (Cream/Yellow) Background Color, Rounded Rectangle App Icon Shape

### Community 9 - "Large Icon (1024px)"
Cohesion: 0.7
Nodes (5): App Icon (1024px) - Bananovnik, Banana bunch illustration, Bananovnik brand identity, Flat icon style with dark outline and white highlight, Yellow rounded-square background (#F2CC4E)

### Community 10 - "Project Setup & Docs"
Cohesion: 0.5
Nodes (4): Rationale: file:// protokol blokuje fetch — nutný HTTP server, README.md — popis aplikace a návod ke spuštění, Lokální HTTP server (python3 -m http.server 8080), Online URL: tomekson.github.io/bananovnik

### Community 11 - "Apple Touch Icon (180px)"
Cohesion: 0.83
Nodes (4): App Icon (180px) — Bananovnik, Banana — central graphic element, Bananovnik brand identity, Yellow/golden rounded-square background

### Community 12 - "Service Worker"
Cohesion: 1.0
Nodes (0): 

### Community 13 - "Dashboard Screen"
Cohesion: 1.0
Nodes (1): screen-dashboard — obrazovka výběru testu

### Community 14 - "Splash Screen"
Cohesion: 1.0
Nodes (1): Splash screen — animovaný úvodní přechod

## Knowledge Gaps
- **42 isolated node(s):** `screen-dashboard — obrazovka výběru testu`, `screen-start — obrazovka nastavení kvízu`, `screen-quiz — obrazovka kvízu`, `screen-results — výsledky testu`, `screen-review — přehled odpovědí` (+37 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Service Worker`** (1 nodes): `sw.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Dashboard Screen`** (1 nodes): `screen-dashboard — obrazovka výběru testu`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Splash Screen`** (1 nodes): `Splash screen — animovaný úvodní přechod`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `S — stav běžícího kvízu (questions, cur, answers, scores, confirmed, retried)` connect `Quiz Core Functions` to `Test Data Pipeline`?**
  _High betweenness centrality (0.093) - this node is a cross-community bridge._
- **Why does `Management EZK, Bc — banka testových otázek (primat.cz)` connect `Management Knowledge Bank` to `Test Data Pipeline`?**
  _High betweenness centrality (0.091) - this node is a cross-community bridge._
- **What connects `screen-dashboard — obrazovka výběru testu`, `screen-start — obrazovka nastavení kvízu`, `screen-quiz — obrazovka kvízu` to the rest of the system?**
  _42 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Quiz Core Functions` be split into smaller, more focused modules?**
  _Cohesion score 0.14 - nodes in this community are weakly interconnected._