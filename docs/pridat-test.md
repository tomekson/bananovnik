# Jak přidat nový test do Banánovníku

## Přehled

Každý test je uložen jako samostatný JSON soubor ve složce `tests/`. Registr všech testů je v souboru `tests/index.json`. Přidání nového testu vyžaduje tři kroky: vytvořit datový soubor, zaregistrovat test a aktualizovat verzi.

---

## Schéma souboru testu (`tests/<id>.json`)

| Pole | Typ | Povinné | Popis |
|---|---|---|---|
| `id` | string | ✓ | Unikátní identifikátor testu, jen písmena/číslice/pomlčky, shodný s názvem souboru |
| `title` | string | ✓ | Název testu zobrazený v dashboardu a na obrazovce nastavení |
| `updatedAt` | string | ✓ | Datum poslední aktualizace otázek ve formátu `YYYY-MM-DD` |
| `rubric` | string | ✓ | Podmínky zkoušky (zobrazeno pod názvem na obrazovce nastavení). Lze použít `\n` pro nový řádek. |
| `questions` | array | ✓ | Pole otázek (viz schéma otázky níže) |

### Schéma otázky

| Pole | Typ | Popis |
|---|---|---|
| `q` | string | Text otázky |
| `opts` | string[] | Pole možností (3–6 položek) |
| `correct` | number[] | Indexy správných odpovědí (0-based). Jeden nebo více. |

Příklady:
- `"correct": [0]` — první možnost je jediná správná
- `"correct": [0, 2, 3]` — první, třetí a čtvrtá jsou správné (vícenásobný výběr)

---

## Kostra souboru testu

```json
{
  "id": "muj-test",
  "title": "Název mého testu",
  "updatedAt": "2026-04-24",
  "rubric": "Zkouškový test: 60 min., 25 otázek po 4 bodech\nSprávná je vždy 1 nebo více odpovědí.",
  "questions": [
    {
      "q": "Text první otázky?",
      "opts": [
        "Možnost A",
        "Možnost B",
        "Možnost C",
        "Možnost D"
      ],
      "correct": [0]
    },
    {
      "q": "Otázka s více správnými odpověďmi?",
      "opts": [
        "Správná A",
        "Špatná B",
        "Správná C"
      ],
      "correct": [0, 2]
    }
  ]
}
```

---

## Checklist přidání testu

### 1. Vytvoř datový soubor
Ulož soubor jako `tests/<id>.json` (např. `tests/marketing.json`). Validuj JSON — v JSON nejsou povoleny trailing commas ani komentáře.

### 2. Zaregistruj test v `index.html`
Najdi konstantu `TESTS_REGISTRY` a přidej záznam:

```js
const TESTS_REGISTRY = [
  { id: 'komunikace', file: 'komunikace.json', title: '...', updatedAt: '...', questionCount: 103 },
  { id: 'marketing', file: 'marketing.json', title: 'Marketing a management', updatedAt: '2026-04-24', questionCount: 87 }
];
```

`questionCount` se zobrazuje v dashboardu; musí odpovídat skutečnému počtu otázek v souboru.

### 3. Přidej soubor do SW precache
V `sw.js` přidej soubor do `TEST_FILES`:

```js
const TEST_FILES = ['./tests/komunikace.json', './tests/marketing.json'];
```

### 4. Aktualizuj verzi (nutné pro invalidaci SW cache)

V těchto čtyřech místech změň verzi (např. z `5.0` na `5.1`):

| Soubor | Kde | Co změnit |
|---|---|---|
| `sw.js` | řádek 1 | `const CACHE = 'bananovnik-v5.1';` |
| `index.html` | hledej `APP_VERSION` | `const APP_VERSION = '5.1';` |
| `index.html` | hledej `manifest.json?v=` | `href="manifest.json?v=5.1"` |
| `version.json` | celý soubor | `{"v":"5.1"}` |

**Proč:** Service worker cachuje starý seznam testů. Bez bumpu verze uvidí existující uživatelé staré data.

### 4. Ověř
- Otevři `http://localhost:8000` (spusť `python3 -m http.server 8000` ve složce projektu)
- Dashboard zobrazuje nový test
- Kliknutí na test přejde na obrazovku nastavení s správným názvem a rubrikou
- Spusť kvíz, ověř fungování otázek

---

## Časté chyby

**Trailing comma v JSON** — JSON nepodporuje čárku za posledním prvkem pole nebo objektu. Zkontroluj pomocí validátoru (např. `node -e "JSON.parse(require('fs').readFileSync('tests/muj-test.json','utf8'))"`)

**`correct` jako řetězce místo čísel** — `"correct": ["0"]` je špatně; musí být `"correct": [0]`

**Nezapomenutý bump SW cache** — pokud nezměníš `CACHE` v `sw.js`, uživatelé s nainstalovanou PWA uvidí starou verzi bez nového testu

**`questionCount` neodpovídá realitě** — číslo v `tests/index.json` je jen informativní (zobrazuje se v dashboardu), ale mělo by souhlasit s počtem otázek v souboru

---

## Zdrojová data

Původní banka otázek pro test Komunikace je v souboru `primat-Komunikace-komunikacni-dovednosti-test-tomek.md` — lze ji použít jako referenci nebo základ pro generování nových otázek.
