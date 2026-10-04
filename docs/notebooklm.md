# NotebookLM (Gemini Notebook) k testům

Každý předmět má vlastní notebook v NotebookLM (účet tomekmasek@gmail.com). Claude Code s ním pracuje přes CLI `notebooklm` z balíčku `notebooklm-py`.

## Mapování testů na notebooky

| Test (`tests/<id>.json`) | Notebook | ID notebooku |
|---|---|---|
| `projektove-rizeni` | Projektové řízení \| VŠEM T4 | `50a4444a-b64a-4461-a7b0-a79fd3d8a8d5` |
| `manazerske-dovednosti` | Manažerské dovednosti \| VŠEM T4 | `7f792179-a373-478d-99ef-e979440a52c2` |
| `inovace` | Inovace \| VŠEM T4 | `b6e1fd3a-e5f7-4d05-ad57-fa4cd8547049` |
| `manazerska-ekonomie` | Manažerská ekonomie \| VŠEM T3 | `b345ad69-97bb-451a-8f63-c9b211c5688b` |
| `politologie-mezinarodni-vztahy` | Politologie a mezinárodní vztahy \| VŠEM T3 | `fec129ea-8456-4e74-82f8-addd43fb57f3` |
| `pravo-v-praxi` | Právo v praxi \| VŠEM T4 | `5d0594fd-6cf3-48e4-8d72-dfa8b29ac3ef` |
| `pravo-prostredi` | Právo a právní prostředí \| VŠEM T3 | `6365dfb6-4bd4-4dd4-a276-89ab8d9df94b` |
| `etika-spolecenska-odpovednost` | Etika a společenská odpovědnost \| VŠEM T3 | `09223f18-0664-4fbe-b618-720dd5dc672e` |
| `management`, `management-stare` | Management \| VŠEM T2 | `2bf26c40-9709-403a-a892-ee137d3d8ff2` |
| `komunikace` | Komunikace a komunikační dovednosti \| VŠEM T2 | `0a6e425c-309a-4690-96b1-e7c9727cb6c4` |
| `anglicky-jazyk` | žádný, nezakládá se | - |

Nový test: doplň řádek sem. ID najdeš přes `notebooklm list --json --no-truncate`.

## Použití

Notebook vždy předávej přes `-n <ID>`, ne přes `notebooklm use`. `use` mění globální stav a při práci na víc předmětech by dotaz šel do špatného notebooku.

```sh
notebooklm source list -n 50a4444a-b64a-4461-a7b0-a79fd3d8a8d5
notebooklm ask -n 50a4444a-b64a-4461-a7b0-a79fd3d8a8d5 --json "Jak se počítá kritická cesta?"
notebooklm source fulltext -n 50a4444a-b64a-4461-a7b0-a79fd3d8a8d5 <source_id> -o /tmp/zdroj.md
```

## Instalace na novém stroji

1. `curl -LsSf https://astral.sh/uv/install.sh | sh` (systémový Python 3.9 nestačí, potřeba 3.10+).
2. `uv tool install --python 3.12 "notebooklm-py[browser]"`
3. `notebooklm login` - otevře prohlížeč, přihlášení se uloží do `~/.notebooklm/profiles/default/storage_state.json`. Soubor nikdy necommituj.
4. `notebooklm skill install --scope project --target claude` - skill pro Claude Code do `.claude/skills/notebooklm/` (složka `.claude/` je v `.gitignore`).
5. Ověření: `notebooklm auth check --test --json` vrátí `"status": "ok"`.
