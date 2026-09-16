# Banánovník - vizuální styl

Referenční dokument pro každý nástroj, který generuje UI, grafiku nebo kód pro Banánovník (Claude CLI, Stitch, Antigravity, Mixboard, Flow, Pomelli). Zdroj pravdy jsou tokeny v `index.html` (blok `:root` a `[data-theme=dark]`). Když se tento dokument a `index.html` rozejdou, platí `index.html` a dokument se opraví.

## Koncept

- **Banánovník v háji.** Světlý motiv je "den v háji": krémová slupka jako podklad, listová zelená jako inkoust i akcent. Tmavý motiv je "noc v háji": listová zelenočerná jako plocha, banánová žlutá jako jediná teplá barva, která se chová jako světlo.
- **Jedna teplá barva.** Žlutá `#f0d540` je stejná v obou motivech a používá se jen na akcent, hover a offsetové stíny. Nikdy jako plocha textu.
- **Offsetový stín je podpis.** Karty, tlačítka, odpovědi a dialog mají za sebou posunutou plochu (`::before`, `translate(3px, 3px)` až `6px`), ne rozmazaný drop shadow. Hover stín zvětší, aktivní stav ho zmenší.
- **Klid, ne efekty.** Animace jsou krátké (130 až 260 ms), jen fade a slide. Žádné gradienty, žádné glassmorphism plochy kromě rozmazaného backdropu dialogu.

## Barevné tokeny

Odvozené odstíny (`*-bg`, `*-mid`, okraje stavů) vznikají výhradně přes `color-mix(in oklab, var(--token) N%, transparent)`. Nová barva do palety nepatří, dokud nejde odvodit z existujícího tokenu.

| Token | Světlý motiv | Tmavý motiv | Použití |
|---|---|---|---|
| `--bg`, `--card` | `#F3EDC4` | `#131C15` | pozadí stránky a karet |
| `--card2` | `#ede7b1` | `#1C281F` | druhá úroveň plochy (dash karty, checkbox) |
| `--opt-bg` | `#FDFAE8` | `#1E2921` | pozadí odpovědi |
| `--line` | `rgba(0,0,0,.05)` | `rgba(255,255,255,.06)` | jemný okraj |
| `--line2` | `rgba(0,0,0,.09)` | `rgba(255,255,255,.13)` | výraznější okraj, výchozí offsetový stín |
| `--text` | `#1F2E23` | `#E6EADA` | základní text |
| `--dim` | `#47554A` | `#9BA898` | sekundární text |
| `--muted` | `#5C685D` | `#889385` | potlačený text, popisky |
| `--primary` | `#007136` | `#63CA84` | akce, aktivní stav, logo |
| `--green` | `#00733E` | `#55C287` | správná odpověď, splněno |
| `--red` | `#B92A2D` | `#F0796E` | špatná odpověď, nebezpečná akce |
| `--amber` | `#955200` | `#E3A64F` | chybějící odpověď, varování |
| `--yellow` | `#f0d540` | `#f0d540` | akcent, hover, offsetový stín |
| `--shadow` | dvojitý měkký stín 4 % / 3 % | 35 % / 28 % | jen výjimečně, standard je offset |

Odvozené: `--primary-bg` 6 % (tmavý 10 %), `--primary-mid` 11 % (20 %), `--green-bg` / `--red-bg` / `--amber-bg` 7 % (12 %), `--yellow-bg` 12 % (9 %), `--yellow-mid` 25 % (20 %).

Kontrast: světlé akcenty jsou ztmavené tak, aby na krémovém podkladu prošly WCAG AA jako text. Tmavý motiv obrací role: světlé akcenty na tmavém listu. Text na `--primary` pozadí je ve světlém motivu bílý, v tmavém `#0A2312`.

## Typografie

- **Písmo:** systémový stack `-apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Segoe UI', Roboto, sans-serif`. Žádné webfonty, žádný Inter.
- **Mono:** `'SF Mono','Fira Code','Cascadia Code',monospace` pouze pro čísla skóre, bodů a klávesové zkratky.
- **Základní řádkování** 1.6, u otázek 1.45.
- **Hierarchie:** hlavní nadpis 30 px / 800 / letter-spacing -0.6 px. Nadpis dialogu 18 px / 700. Název karty a otázka 16 až 17 px / 700 / -0.2 px. Tělo 15 px. Popisek 11.5 až 13 px / 500 až 600. Logo název 11 px, verzálky, letter-spacing 2 px.
- **Zalamování:** nadpisy `text-wrap: balance`, text otázky `text-wrap: pretty`. Progressive enhancement, bez fallbacku.

## Tvary a rozestupy

- **Poloměry:** `--r` 14 px pro karty, tlačítka a odpovědi. `--r-sm` 9 px pro menší prvky. Checkbox odpovědi 6 px. Pilulky a odznaky 100 px. Dialog 20 px jen nahoře (bottom sheet).
- **Okraje:** 2 px `--line2` na interaktivních kartách, 1.5 px na dash kartách a chipech, 1 px na dialogu.
- **Padding:** karty 14 až 16 px svisle, 15 až 18 px vodorovně. Primární tlačítko 16 px / 24 px. Obrazovka 32 px / 18 px plus `env(safe-area-inset-bottom)`.
- **Šířka obsahu:** max 440 px na startu, 480 px v dialogu. Layout je mobile-first, jeden sloupec, na desktopu se jen centruje.
- **Mezery:** flex gap 9 až 18 px. Žádné margin hacky, rozestupy drží rodič.

## Komponenty

- **Primární tlačítko** (`.btn-start`): plná `--primary`, bílý text, offset `--yellow-mid` s 2 px `--yellow` okrajem posunutý o 3 px, hover 5 px.
- **Volba / karta** (`.mode-card`, `.set-pill`, `.dash-card`): plocha `--card` nebo `--card2`, offset `--line2`. Hover přebarví offset na `--yellow-mid` a okraj na `--yellow`. Aktivní stav: okraj `--primary`, pozadí `--primary-bg`, offset dostane 2 px `--yellow` rám.
- **Odpověď** (`.opt`): pozadí `--opt-bg`, offset žlutá 10 %. Stavy `.sel` primary, `.ok` green, `.bad` red, `.miss` amber, vždy pozadí `*-bg` a okraj `color-mix` 25 až 30 % z tokenu. Checkbox `.opt-box` 22 px.
- **Odznaky** (`.badge-pass`, `.badge-fail`, `.exam-note-*`): pilulka nebo 8 px blok, text v barvě stavu, pozadí `*-bg`, okraj 15 až 20 %.
- **Dialog** (`.dialog`): nativní `<dialog>` přes `showModal()`, bottom sheet, max výška `100dvh - 32px`, tělo roluje, tlačítka zůstávají vidět. Backdrop tmavý s blur 4 px. Offset stín nad horní hranou. Autofocus na bezpečné tlačítko, klávesa x zavírá.
- **Logo:** čtverec 44 px s poloměrem 12 px, `--primary-bg` plocha, žlutý offset posunutý doleva nahoru o 3 px (jediný prvek se záporným offsetem).

## Pohyb

- **Délky:** přechody 100 až 150 ms, vstup obrazovky `fadeUp` 260 ms, přepnutí otázky slide 130 ms ven a 180 ms dovnitř, dialog `slideUp` 250 ms `cubic-bezier(.4,0,.2,1)`.
- **Reduced motion:** `prefers-reduced-motion: reduce` vypíná přechody offsetů, posun aktivního stavu i animaci dialogu. Každá nová animace musí mít tuto větev.
- **Zakázáno:** parallax, bounce, nekonečné smyčky mimo splash, animace barvy textu.

## Pravidla pro generované výstupy

- **Stitch, Antigravity, jiný generátor:** výstup se nikdy nevkládá přímo. Claude ho přepíše na tokeny výše, systémový font a offsetové stíny. Pokud návrh potřebuje barvu, která v tabulce není, návrh se upraví, ne paleta.
- **Mixboard, Flow, Pomelli:** grafika používá krém `#F3EDC4`, list `#007136` nebo `#131C15`, banán `#f0d540`. Motiv banánovníku a listů, ploché tvary s offsetovým stínem, žádné 3D rendery ani fotografie.
- **Nový komponent** musí projít oběma motivy (přepínač `data-theme`), iPhone SE šířkou 320 px, klávesnicí a `prefers-reduced-motion`.
- **Kontrola:** po změně stylu porovnat screenshoty obou motivů obrazovek start, kvíz, výsledek a dialog.
