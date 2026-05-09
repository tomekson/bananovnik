---
type: community
cohesion: 0.14
members: 19
---

# Quiz Core Functions

**Cohesion:** 0.14 - loosely connected
**Members:** 19 nodes

## Members
- [[PASS_THRESHOLD = 0.51 — práh úspěšnosti testu]] - code - index.html
- [[S — stav běžícího kvízu (questions, cur, answers, scores, confirmed, retried)]] - code - index.html
- [[bananaConfetti()  spawnBurst() — animace banánů při úspěchu]] - code - index.html
- [[cfg — konfigurace kvízu (mode, count, fb, qorder, oorder, study)]] - code - index.html
- [[mainBtn() — potvrzení odpovědi nebo přechod na další otázku]] - code - index.html
- [[openReview() — zobrazení přehledu odpovědí]] - code - index.html
- [[renderQ() — vykreslení aktuální otázky a možností]] - code - index.html
- [[retryQ() — opakování jednotlivé otázky (přeskládání možností)]] - code - index.html
- [[retryWrong() — opakování chybně zodpovězených otázek]] - code - index.html
- [[screen-quiz — obrazovka kvízu]] - code - index.html
- [[screen-results — výsledky testu]] - code - index.html
- [[screen-review — přehled odpovědí]] - code - index.html
- [[screen-study — procházení otázek (study mode)]] - code - index.html
- [[setCount(n) — nastavení počtu otázek]] - code - index.html
- [[setMode(m) — přepínání režimu všechnyrozsah]] - code - index.html
- [[setSeg(key, val) — přepínání segmentovaných ovládacích prvků]] - code - index.html
- [[showResults() — výpočet a zobrazení výsledků]] - code - index.html
- [[startQuiz() — sestavení poolu otázek a spuštění kvízu]] - code - index.html
- [[startStudy() — spuštění procházení otázek]] - code - index.html

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Quiz_Core_Functions
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Test Data Pipeline]]

## Top bridge nodes
- [[S — stav běžícího kvízu (questions, cur, answers, scores, confirmed, retried)]] - degree 9, connects to 1 community