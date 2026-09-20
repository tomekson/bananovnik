# Jak přidat nový test do Banánovníku

Aktuální k verzi 9.41 (20. září 2026). Když se tento návod a `index.html` rozejdou, platí `index.html` a návod se opraví.

## Přehled

Každý test je jeden JSON soubor ve složce `tests/`. Registr testů je konstanta `TESTS_REGISTRY` v `index.html` (soubor `tests/index.json` neexistuje, starší verze návodu ho uváděla omylem). Přidání testu má pět kroků: datový soubor, záznam v registru, precache v `sw.js`, bump verze, ověření v prohlížeči.

---

## Schéma souboru testu (`tests/<id>.json`)

| Pole | Typ | Povinné | Popis |
|---|---|---|---|
| `id` | string | ano | Identifikátor, jen písmena/číslice/pomlčky, shodný s názvem souboru i s `id` v registru |
| `title` | string | ano | Název testu, musí souhlasit s `title` v registru |
| `updatedAt` | string | ano | Datum poslední aktualizace otázek, `YYYY-MM-DD` |
| `rubric` | string | ano | Podmínky zkoušky pod názvem na obrazovce nastavení. `\n` dělá nový řádek |
| `format` | object | ano | Jak se v testu odpovídá, viz níže |
| `exam` | object | ano | Bodování zkoušky, viz níže |
| `questions` | array | ano | Otázky, viz níže |
| `sets` | array | ne | Tematické sady, viz níže. Když je uvedeš, dej do registru `hasSets: true` |
| `openQuestions` | string[] | ne | Seznam otevřených otázek ke zkoušce. Aplikace je zatím nikde nezobrazuje, jen je drží u testu |

### `format`

```json
"format": { "type": "multiple-choice", "correctAnswers": "one-or-more" }
```

`correctAnswers` řídí větu pod rubrikou (funkce `formatCorrectAnswersLabel`) a text, který se kopíruje tlačítkem **Kopírovat otázku**:

| Hodnota | Zobrazí se |
|---|---|
| `"one-or-more"` | Správná je 1 nebo více odpovědí. |
| `"exactly-one"` | Správná je právě 1 odpověď. |
| číslo, např. `3` | Správné jsou právě 3 odpovědi. |

Rubrika už tuhle větu psát nemusí, aplikace ji přidá sama.

### `exam`

```json
"exam": { "testPoints": 60, "openPoints": 40, "passPoints": 51, "questionCount": 12, "openCount": 2 }
```

| Pole | Význam |
|---|---|
| `testPoints` | Body za uzavřenou (testovou) část ostré zkoušky |
| `openPoints` | Body za otevřené otázky. Bez otevřených otázek `0` |
| `passPoints` | Hranice složení zkoušky. Na VŠEM 51 bodů (nejnižší hranice klasifikace „dobře" podle sborníku NR) |
| `questionCount` | Počet uzavřených otázek v ostré zkoušce |
| `openCount` | Počet otevřených otázek v ostré zkoušce |

Kde se to projeví:

- **Simulace zkoušky** losuje `questionCount` otázek.
- **Číselné sady** v zóně procvičování se krájí po `questionCount` otázkách (bez `exam` po 20).
- **Hláška u výsledku** počítá `testPoints × procento úspěšnosti` a porovnává s `passPoints`. Při `openCount > 0` píše, kolik bodů by ještě bylo potřeba z otevřených otázek, jinak píše celkové body.

### Schéma otázky

| Pole | Typ | Popis |
|---|---|---|
| `q` | string | Text otázky |
| `opts` | string[] | Možnosti, ve stávajících testech 3 až 6 |
| `correct` | number[] | Indexy správných odpovědí, **0-based**. Jeden nebo více |
| `img` | string | Nepovinné. Cesta k obrázku se zadáním relativně ke složce `tests/`, např. `img/projektove-rizeni/q055.jpg` |

```json
{
  "q": "Otázka s více správnými odpověďmi?",
  "opts": ["Správná A", "Špatná B", "Správná C"],
  "correct": [0, 2]
}
```

Obrázek se ukazuje v testu, v Active recall, v přehledu odpovědí i v tisku; klik otevře plnou velikost. Soubory patří do `tests/img/<id-testu>/`.

### `sets` (tematické sady)

```json
"sets": [
  { "name": "Typy a formy inovací", "q": [2, 16, 28, 32, 40, 41, 47, 51, 52] },
  { "name": "Tvořivost a inovátor", "q": [7, 8, 13, 15, 22, 25, 29, 33, 39] }
]
```

- **Indexy jsou 1-based** (aplikace počítá `n - 1`). Index mimo rozsah se tiše ignoruje, takže překlep nevyhodí chybu, jen zmizí otázka.
- **Sady musí pokrývat všechny otázky** a nemají se překrývat. Vybraná témata se slévají do jednoho testu bez duplicit.
- **Řaď od nejlehčího tématu k nejtěžšímu**, nebo podle struktury sylabu. V rozhraní se ukazují první 4 sady, zbytek je za tlačítkem „Zobrazit všech N témat" - co je nahoře, to student uvidí první.
- Název drž krátký, vejde se do dlaždice vedle počtu otázek.

### Sporné otázky

Když si u otázky nejsi jistý klíčem (rozpory v komentářích na Primátu, částečné body u autora, neověřeno z přednášek), přidej na konec textu otázky ` (bez záruky)`:

```json
{ "q": "Prokrastinace je: (bez záruky)", "opts": ["..."], "correct": [1, 2] }
```

Žádné zvláštní pole pro to není, značka je součástí textu. Klíč se nechává podle zdroje, ale student ví, že tady může být jinak.

---

## Záznam v registru (`index.html`, `TESTS_REGISTRY`)

```js
{
  id: 'inovace',
  file: 'inovace.json',
  title: 'Inovace',
  updatedAt: '2026-09-20',
  questionCount: 54,
  hasSets: true,
  draft: true
}
```

| Pole | Popis |
|---|---|
| `id`, `file`, `title`, `updatedAt` | Musí souhlasit s JSON souborem (`file` je jméno souboru bez cesty) |
| `questionCount` | Počet otázek, zobrazuje se na dlaždici. Musí souhlasit s délkou `questions` |
| `hasSets` | `true`, když má test `sets`. Přidá na dlaždici ikonu tematických sad |
| `draft` | `true` = štítek **Pracovní verze** (žlutý) na dlaždici i v detailu. Pro test, jehož klíč ještě není ověřený zkouškou |
| `retired` | `true` = štítek **✓ Splněno** a ztmavená dlaždice. Pro už složený předmět |

Splněné testy se v dashboardu řadí nakonec, ostatní zůstávají v pořadí registru - nový test patří na začátek pole.

---

## Checklist přidání testu

1. **Ověř, že máš aktuální main.** `git fetch && git status` - upstream mohl mezitím obsadit číslo verze i přidat konvence, které tady ještě nejsou popsané.
2. **Vytvoř `tests/<id>.json`** podle schématu výše. JSON nesnese trailing comma ani komentáře.
3. **Zaregistruj test** v `TESTS_REGISTRY` v `index.html`.
4. **Přidej soubor do precache** v `sw.js`, konstanta `TEST_FILES`.
5. **Zvyš verzi na čtyřech místech** (bez toho uvidí uživatelé s nainstalovanou PWA stará data):

   | Soubor | Kde | Co změnit |
   |---|---|---|
   | `sw.js` | řádek 1 | `const CACHE = 'bananovnik-v9.42';` |
   | `index.html` | `APP_VERSION` | `const APP_VERSION = '9.42';` |
   | `index.html` | `manifest.json?v=` | `href="manifest.json?v=9.42"` |
   | `version.json` | celý soubor | `{"v":"9.42"}` |

6. **Zvaliduj strojově:**

   ```bash
   node -e "
   const fs=require('fs');
   const d=JSON.parse(fs.readFileSync('tests/inovace.json','utf8'));
   const idx=(d.sets||[]).flatMap(s=>s.q);
   console.log('otázky',d.questions.length,'| sady pokrývají',new Set(idx).size,'| duplicity',idx.length-new Set(idx).size);
   const html=fs.readFileSync('index.html','utf8');
   [...html.matchAll(/<script(?![^>]*src=)[^>]*>([\s\S]*?)<\/script>/g)].forEach(m=>new Function(m[1]));
   const reg=eval(html.match(/const TESTS_REGISTRY = \[[\s\S]*?\n\];/)[0].replace('const TESTS_REGISTRY =',''));
   for(const t of reg){const f=JSON.parse(fs.readFileSync('tests/'+t.file,'utf8'));
     const bad=[]; if(f.questions.length!==t.questionCount)bad.push('count');
     if(f.id!==t.id)bad.push('id'); if(f.title!==t.title)bad.push('title');
     if(!!t.hasSets!==!!(f.sets&&f.sets.length))bad.push('hasSets');
     console.log((bad.length?'CHYBA '+bad.join(','):'ok')+' '+t.id);}
   "
   ```

7. **Ověř v prohlížeči** (`python3 -m http.server 8080 --bind 127.0.0.1`, pak `http://127.0.0.1:8080`): dlaždice se správným počtem otázek a štítkem, detail s rubrikou a sadami, výběr sady dá očekávaný počet otázek, kvíz vyhodnotí správnou odpověď, simulace zkoušky losuje `exam.questionCount` otázek.

Service worker drží starou verzi i na localhostu. Když se změna nezobrazí, přidej k URL parametr (`?v=2`) nebo si v prohlížeči smaž cache.

---

## Časté chyby

- **Kolize verze.** Bez `git fetch` před bumpem snadno použiješ číslo, které už upstream zabral pro jinou změnu.
- **Sady jako 0-based.** Indexy v `sets` jsou 1-based a chyba se neprojeví chybou, jen chybějící nebo cizí otázkou v sadě.
- **Sady nepokrývají všechny otázky.** Otázka mimo všechny sady je dostupná jen v režimu „Vše" - zkontroluj pokrytí skriptem z bodu 6.
- **`questionCount` v registru neodpovídá souboru.** Číslo na dlaždici pak lže.
- **`correct` jako řetězce.** `"correct": ["0"]` je špatně, musí být `"correct": [0]`.
- **Trailing comma v JSON.** JSON nepodporuje čárku za posledním prvkem.
- **Zapomenutý `hasSets`.** Test má sady, ale na dlaždici chybí ikona.
- **Dvě otázky se stejným textem nejsou nutně duplicita.** Na Primátu se běžně opakuje zadání s jinými možnostmi - kontroluj i `opts`, než něco smažeš.

---

## Odkud brát data

Většina testů pochází z Primátu (primat.cz). Postup pro jeden test:

1. **Přihlaš se.** `POST /snippet/auth/login`, Symfony formulář `auth_login_form[email|password|next|_token]`, token vyčti z `GET /prihlaseni`. Přihlášení drží session cookie.
2. **Najdi `testId`.** Je v detailu testu v odkazu tlačítka Spustit (`/testovani/start/XXXXXX`) i v `window.reactTestingModule`. Detail testu vrací `GET /api/rest/question/tests/{testId}`.
3. **Kup a spusť sadu.** `POST /api/rest/question/set-start/{testId}` s tělem `{"filter":"all","filterParams":null,"count":<všechny otázky>,"showSolution":"immediate","orderOptions":"order","orderQuestions":"order","limitQuestion":null,"limitTest":null}`. Tady se odečtou banány, dál je test 30 dní zdarma.
4. **Vyber otázky.** Odpověď obsahuje `nextQuestion` včetně `options[].correct`. Dál cykluj `POST /api/rest/question/set/{setId}/skip-question` s `{"questionId": "<id>"}`, dokud se otázky neopakují.
5. **Přečti komentáře.** `POST /api/komentare/komentare` s `{"primitiveId": <id>}`. `primitiveId` je v HTML detailu v atributu `discussion-vo`. Komentáře hlásí nové a sporné otázky a bývá v nich skladba ostré zkoušky.

Podmínky zkoušky ale ber ze sylabu předmětu (`~/projects/vsem/md-export/00-Studium-a-administrativa/Sylaby-prirucky-pokyny/`), ne z komentářů - studenti v nich popisují svůj výsledek, ne hranici složení. Pozor i na podobně pojmenované předměty (Inovace vs. Inovace na webu mají jiný test).
